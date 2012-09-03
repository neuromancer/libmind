I=-Iinclude -I/usr/include/python2.7
L=-L/usr/lib -lpython2.7 -fPIC
S=-c src/*.c

all: hnj.so

hnj.so: hnjalloc.o hnjmodule.o hyphen.o
	gcc -shared src/hnjalloc.o src/hnjmodule.o src/hyphen.o $I $L -o hnj.so

hnjalloc.o: src/hnjalloc.c
	gcc -c src/hnjalloc.c $I $L -o src/hnjalloc.o

hnjmodule.o: src/hnjmodule.c
	gcc -c src/hnjmodule.c $I $L -o src/hnjmodule.o

hyphen.o: src/hyphen.c
	gcc -c src/hyphen.c $I $L -o src/hyphen.o

clean:
	rm hnj.so
	rm src/*.o
