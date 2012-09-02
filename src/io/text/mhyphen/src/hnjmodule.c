#include "Python.h"
#include "structmember.h"
#include "hyphen.h"
#include "string.h"

/* String constants for calls of Py_Unicode_FromEncodedObject etc.*/
static const char unicode_errors[] = "strict";



/* is raised if hnj_hyphen returns an error while trying to hyphenate a word*/
static PyObject *ErrorObject;

/* ----------------------------------------------------- */

/* Declarations for objects of type hyphenator_ */

/* type object to store the hyphenation dictionary. Its only method is 'apply' which calls the
core function 'hnj_hyphenate2'' from the wrapped library 'hnj_hyphen-2.3' */
typedef struct {
    PyObject_HEAD
    HyphenDict *dict;
    int lmin, rmin, compound_lmin, compound_rmin;
} HyDictobject;

static PyTypeObject HyDict_type;



/* ---------------------------------------------------------------- */

static char HyDict_apply__doc__[] =
"SUMMARY:\n\
apply(word: unicode object, mode: int) -> hyphenated word (return type depends on value of mode)\n\n\
Note: 'hnj' should normally be called only from the convenience interface provided by\
the hyphen.hyphenator class.\n\n\
word: must be lower-cased to be hyphenated correctly. Through the flags in mode,\n\
        the caller can provide information on whether the word was originally capitalized, \n\
        lower-cased or upper-cased.  Capital letters are restored \n\
        according to the value of 'mode'. The encoded representation of 'word'\n\
        may have at most 100 bytes including the terminating '\0'.\n\
mode: the 3 least significant bits are interpreted as flags with the following meaning:\n\
        - mode & 1 = 0: return a string with '=' inserted at the hyphenation points\n\
        - mode & 1 = 1: return a list of lists of the form [before_hyphen, after_hyphen]\n\
        - mode & 2 = 1: return a capitalized word\n\
        - mode & 4 = 1: return an upper-cased word\n";

/* get a pointer to the nth 8-bit or UTF-8 character of the word */
/* This is required because some operations are done at utf8 string level. */
static char * hindex(char * word, int n, int utf8) {
    int j = 0;
    while (j < n) {
        j++;
        word++;
        while (utf8 && ((((unsigned char) *word) >> 6) == 2)) word++;
    }
    return word;
}


/* Depending on the value of 'mode', convert a utf8 C string to PyUnicode or PyString (utf8), handle also
    capitalization and upper case words. */
static PyObject * prepare_result(char *word, char *encoding, int mode)
{
    Py_UNICODE * ch_u;
    PyObject *result;
    int len_s, i;

    /* first convert the C string to unicode. */

    if (!(result = PyUnicode_Decode(word, strlen(word), encoding, unicode_errors)))
        return NULL;
    if (mode & 4) { /* capitalize entire word */
        ch_u = PyUnicode_AS_UNICODE(result);
        len_s = PyUnicode_GetSize(result);
        for (i=0; i <= len_s; i++)
        {
            *ch_u = Py_UNICODE_TOUPPER(*ch_u);
            ch_u++;
        }
    }
    else
    {
        if (mode & 2) { /* capitalize first letter */
            ch_u = PyUnicode_AS_UNICODE(result);
            *ch_u = Py_UNICODE_TOUPPER(*ch_u);
        }
    }
    /* return a unicode object */
    return result;
}

/* core function of the hyphenator_ object type */
static PyObject *
HyDict_apply(HyDictobject *self, PyObject *args)
{
    const char separator[] = "=";
    char  *hyphenated_word, *hyphens, *word_str;
    char ** rep = NULL;
    char r;
    int * pos = NULL;
    int * cut = NULL;
    unsigned int wd_size, hyph_count, i, j, k, mode;
    PyObject *result, *s1, *s2, *separator_u = NULL;
/* mode:
   bit0 === 1: return a tuple, otherwise a word with '=' inserted at the positions of possible hyphenations.
   bit1 == 1: word must be capitalized before returning
  bit2 == 1: entire word must be uppered before returning  */


    /* parse and check arguments */
    if (!PyArg_ParseTuple(args, "esi", &self->dict->cset, &word_str, &mode))
          return NULL;
    wd_size = strlen(word_str);
    if (wd_size >= MAX_CHARS)
    {
        PyErr_SetString(PyExc_ValueError, "Word to be hyphenated may have at most 100 characters.");
        PyMem_Free(word_str);
        return NULL;
    }

    /* allocate memory for the return values of the core function hnj_hyphenate2*/
    hyphens = (char *) PyMem_Malloc(wd_size + 5);
    hyphenated_word = (char *) PyMem_Malloc(wd_size * 3);

    /* now actually try the hyphenation*/
    if (hnj_hyphen_hyphenate3(self->dict, word_str, wd_size, hyphens,
        hyphenated_word, &rep, &pos, &cut,
        self->lmin, self->rmin, self->compound_lmin, self->compound_rmin))
    {
        PyMem_Free(hyphens);
        PyMem_Free(hyphenated_word);
        PyMem_Free(word_str);
        PyErr_SetString(ErrorObject, "Cannot hyphenate word.");
        return NULL;
    }
    /* Count possible hyphenations. This is done by checking bit 0 of each */
    /* char of 'hyphens' which is 0 if and only if the word can be hyphened */
    /* at that position. Then proceed to */
    /* the real work, i.d. returning a unicode object with inserted '=' at each */
    /* possible hyphenation, or return a list of lists of two unicode objects */
    /* representing a possible hyphenation each. Note that the string */
    /* is useful only in languages without non-standard hyphenation, as */
    /* the string could contain more than one replacement, whereas */
    /* we are only interested in one replacement at the hyphenation position */
    /* we choose. */
    /* If no hyphenations were found, a string with 0 inserted '=', i.e. the original word, */
    /* or an empty list (with 0 pairs) is returned. */
    hyph_count = 0;
    for (i=0; (i+1) < strlen(hyphens); i++)
    {
        if (hyphens[i] & 1) hyph_count++;
    }
    /* Do we need to return a string with inserted '=', or a list of pairs? */
    if (!(mode & 1))
    {
        /* Prepare for returning a unicode obj of the form 'before_hyphen=after_hyphen.  */
        if (!(result = prepare_result(hyphenated_word, self->dict->cset, mode)))
        {
            PyMem_Free(hyphenated_word);
            PyMem_Free(word_str);
            PyMem_Free(hyphens);
            return NULL;
        }
        PyMem_Free(hyphenated_word);
    }
    else
    {
    PyMem_Free(hyphenated_word);
        /* construct a list of lists of two unicode objects. Each inner list */
        /* represents a possible hyphenation. */


        /* First create the outer list. Each element will be a list of two strings or unicode objects. */
        if (!(result = PyList_New(hyph_count)))
        {
            PyMem_Free(hyphens);
            PyMem_Free(word_str);
            return NULL;
        }
        /* now fill the resulting list from left to right with the pairs */
        j=0; hyph_count = 0;
        /* The following is needed to split the word (in which an '=' indicates the */
        /* hyphen position) */
        separator_u = PyUnicode_Decode(separator, 1, self->dict->cset, unicode_errors);

        for (i = 0; (i + 1) < strlen(word_str); i++)
        {
            /* j-th character utf8? Then just increment j */
            if (self->dict->utf8 && ((((unsigned char) word_str[i]) >> 6) == 2)) continue;

            /* Is here a hyphen? */
            if ((hyphens[j] & 1))
            {
                /* Build the hyphenated word at C string level. */
                /* first, handle non-standard hyphenation with replacement. */
                if (rep && rep[j])
                {
                    /* determine the position within word_str where to insert rep[j] */
                    /* do the replacement by appending the three substrings: */
                    hyphenated_word = (char *) PyMem_Malloc(strlen(word_str) + strlen(rep[j])+1);
                    k = hindex(word_str, j - pos[j] + 1, self->dict->utf8) - word_str;
                    r = word_str[k]; word_str[k] = 0;
                    strcpy(hyphenated_word, word_str);
                    strcat(hyphenated_word, rep[j]);
                    word_str[k] = r;
                    strcat(hyphenated_word, hindex(word_str + k, cut[j], self->dict->utf8));
                }
                else
                {
                    /* build the word in case of standard hyphenation. */
                    /* An '=' will be inserted so that the */
                    /* resulting string has the same format as in the non-standard case. */
                    hyphenated_word = (char *) PyMem_Malloc(strlen(word_str) + 2);
                    k = hindex(word_str, j + 1, self->dict->utf8) - word_str;
                    r = word_str[k]; word_str[k] = 0;
                    strcpy(hyphenated_word, word_str);
                    strcat(hyphenated_word, separator);
                    word_str[k] = r;
                    strcat(hyphenated_word, word_str + k);
                }
                /* Now prepare the resulting unicode object according to the value of mode */
                if (!(s1 = prepare_result(hyphenated_word, self->dict->cset, mode)))
                {
                    PyMem_Free(hyphenated_word);
                    PyMem_Free(hyphens);
                    PyMem_Free(word_str);
                    return NULL;
                }
                PyMem_Free(hyphenated_word);
                
                /* split it into two parts at the position of the '=' */
                /* and write the resulting list into the tuple */
                if (!((s2 = PyUnicode_Split(s1, separator_u, 1)) &&
                    (!PyList_SetItem(result, hyph_count++, s2))))
                {
                    Py_XDECREF(s2);
                    Py_DECREF(s1);
                    PyMem_Free(hyphens);
                    PyMem_Free(word_str);
                    return NULL;
                }
                Py_DECREF(s1);
            } /* finished with current hyphen */
            j++;
        } /* for loop*/
        Py_DECREF(separator_u);
    } /* end of else construct a list */
    PyMem_Free(hyphens);
    PyMem_Free(word_str);
    return result;
}


static struct PyMethodDef HyDict_methods[] = {
	{"apply",	(PyCFunction)HyDict_apply,	METH_VARARGS,	HyDict_apply__doc__},

	{NULL,		NULL}		/* sentinel */
};

/* ---------- */



static void
HyDict_dealloc(HyDictobject *self)
{
	if (self->dict) hnj_hyphen_free(self->dict);
	self->ob_type->tp_free((PyObject*) self);
}

static int
HyDict_init(HyDictobject *self, PyObject *args) {
    char* fn;
    if (!PyArg_ParseTuple(args, "siiii", &fn, &self->lmin, &self->rmin,
        &self->compound_lmin, &self->compound_rmin))
  		return -1;
    if (!(self->dict = hnj_hyphen_load(fn)))
    {
        if (!PyErr_Occurred()) PyErr_SetString(PyExc_IOError, "Cannot load hyphen dictionary.");
        return -1;
    }
    return 0;
}


static char HyDict_type__doc__[] =
"Wrapper class for the hnj_hyphen library contained in this module.\n\n\
Usage: hyphenator_(dict_file_name: string, lmin, rmin, compound_lmin, compound_rmin: integer)\n\
The init method will try to load a hyphenation dictionary with the filename passed.\n\
If an error occurs when trying to load the dictionary, IOError is raised.\n\
Dictionary files compatible with hnj can be downloaded at the OpenOffice website.\n\n\
This class should normally be instantiated only by the convenience interface provided by\n\
the hyphen.hyphenator class.\n"
;



static PyTypeObject HyDict_type = {
	PyObject_HEAD_INIT(NULL)
	0,				/*ob_size*/
	"hyphenator_",			/*tp_name*/
	sizeof(HyDictobject),		/*tp_basicsize*/
	0,				/*tp_itemsize*/
	/* methods */
	(destructor)HyDict_dealloc,	/*tp_dealloc*/
	(printfunc)0,		/*tp_print*/
	0,	/*tp_getattr*/
	(setattrfunc)0,	/*tp_setattr*/
	(cmpfunc)0,		/*tp_compare*/
	(reprfunc)0,		/*tp_repr*/
	0,			/*tp_as_number*/
	0,		/*tp_as_sequence*/
	0,		/*tp_as_mapping*/
	(hashfunc)0,		/*tp_hash*/
	(ternaryfunc)0,		/*tp_call*/
	(reprfunc)0,		/*tp_str*/

	0,                         /*tp_getattro*/
0,                         /*tp_setattro*/
0,                         /*tp_as_buffer*/
Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
HyDict_type__doc__, /* Documentation string */
0,		               /* tp_traverse */
0,		               /* tp_clear */
0,		               /* tp_richcompare */
0,		               /* tp_weaklistoffset */
0,		               /* tp_iter */
0,		               /* tp_iternext */
HyDict_methods,             /* tp_methods */
0,             /* tp_members */
0,                         /* tp_getset */
0,                         /* tp_base */
0,                         /* tp_dict */
0,                         /* tp_descr_get */
0,                         /* tp_descr_set */
0,                         /* tp_dictoffset */
(initproc)HyDict_init,      /* tp_init */
0,                         /* tp_alloc */
0,                 /* tp_new */
};


/* End of code for hyphenator_ objects */
/* -------------------------------------------------------- */


/* List of methods defined in the module */

static struct PyMethodDef hnj_methods[] = {

	{NULL,	 (PyCFunction)NULL, 0, NULL}		/* sentinel */
};



static char hnj_module_documentation[] =
"This C extension module is a wrapper around the hyphenation library 'hyphen-2.4' (2008-05).\n\
It should normally be imported and invoked only by the convenience interface provided\n\
by the hyphen.hyphenator class.\n"
;

PyMODINIT_FUNC
inithnj(void)
{
	PyObject *m, *d;

HyDict_type.tp_new = PyType_GenericNew;
if (PyType_Ready(&HyDict_type) < 0)
    return;

	/* Create the module and add the functions */
	m = Py_InitModule3("hnj", hnj_methods,
		hnj_module_documentation);
  if (m == NULL)
    return;

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);
	ErrorObject = PyString_FromString("hnj.error");
	PyDict_SetItemString(d, "error", ErrorObject);

	Py_INCREF(&HyDict_type);
    PyModule_AddObject(m, "hyphenator_", (PyObject *)&HyDict_type);


	/* Check for errors */
	if (PyErr_Occurred())
		Py_FatalError("cannot initialize module hnj.");
}
