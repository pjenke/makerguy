#ifndef INDEXED_LIST_H
#define INDEXED_LIST_H

#include "Arduino.h"

template<class T> 
class IndexedList
{
  public:
    IndexedList();
    void add(T element);
    T get(int index);
    int getSize();
    void insertAt(int index, T element);
    void clear();
    
  private:
    T* elements;
    int numElements;
    int maxNumElements = 2;
};

template <class T>
IndexedList<T>::IndexedList(){
  elements = new T[maxNumElements];
  numElements = 0;
}

template <class T>
void IndexedList<T>::add(T element){

  if ( numElements == maxNumElements ){
    maxNumElements *= 2;
    T* tmp = new T[maxNumElements];
    for ( int i = 0; i < numElements; i++ ){
      tmp[i] = elements[i];
    }
    elements = tmp;
  }
  
  elements[numElements] = element;
  numElements++;
}

template <class T>
T IndexedList<T>::get(int index){
  return elements[index];
}

template <class T>
int IndexedList<T>::getSize(){
  return numElements;
}

template <class T>
void IndexedList<T>::insertAt(int index, T element){
  for ( int i = numElements; i > index; i++){
    elements[i] = elements[i-1];  
  }
  elements[index] = element;
  numElements++;
}

template <class T>
void IndexedList<T>::clear(){
  numElements = 0;
}

#endif
