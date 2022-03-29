# Intertext: database

У нас есть проект по исследованию **интертекстуальности** на материале русской поэзии

1. Метадата по поэтам
    
    ```json
    name:
    year_born:
    year_dead:
    poems: [Object1, Object2, Object3, ..., ObjectN]
    books: [Object1, Object2]
    ```
    
2. Метадата по стиху
    
    ```json
    poem_name:
    poem_name_2:
    author:
    text:
    book: Object
    comment: {
    	author: 
    	text:
    }
    ```
    
3.  Метадата по отсылкам:
    
    ```json
    poem: Object
    author: Object
    start:
    finish:
    text:
    person: Object
    ```
    
4. Метадата по сборнику 
    
    ```json
    book_name:
    year_published:
    publishing_company: ?
    ```
    
5. Леммы
    
    ```json
    lemma:
    freq:
    docs: [Object1, Object2, ..., ObjectN]
    ```
