2021-08-09 | 신규 작성

---

## Pagination

### [📚 **Bootstrap Reference | Pagination**](https://getbootstrap.com/docs/4.4/components/pagination/)

### 1. 테스트용 데이터 입력
* **`config/settings.py` 등록**  
![Pagination_App_Definition](https://user-images.githubusercontent.com/17983434/128659381-c44202f1-8e40-4e37-8c21-38fd4233630f.PNG)

* **`pagination/models.py` 작성**  
![Pagination_Create_Model](https://user-images.githubusercontent.com/17983434/128659626-bbfab579-c91a-49f0-a72c-fe3e5001f893.PNG)

* **`python manage.py makemigrations & migrate` 실행**
    * **사용 중인 DB에 맞게 설정(<u>MariaDB 기준</u>)**  
    ![Pagination_Migrate](https://user-images.githubusercontent.com/17983434/128659900-02a57ff1-ba04-4c2a-a985-260acd4f616d.PNG)

    * **아래의 두 명령어를 실행**
    ```plaintext
    $ python manage.py makemigrations
    ```
    ```plaintext
    $ python manage.py migrate
    ```

* **`config/urls.py` 주소 생성**  
![Pagination_urls](https://user-images.githubusercontent.com/17983434/128660370-93b9ee61-4002-44dc-8d63-8573f84e50b1.PNG)

* **`pagination/views.py` 데이터 입력 기능 함수 작성**  
![Pagination_views](https://user-images.githubusercontent.com/17983434/128660542-4a032ead-e506-41dc-881e-e5d13d538b4a.PNG)

* **서버 구동 후 DB에 테스트 데이터 등록**
```plaintext
$ python manage.py runserver
```
![Pagination_Insert_Data](https://user-images.githubusercontent.com/17983434/128660783-b77168ab-38df-4752-8e76-3a6246c6903f.PNG)  
![Pagination_DB](https://user-images.githubusercontent.com/17983434/128661097-b9b4bfde-67e2-4d9c-834f-56844abd21bd.PNG)

### 2. Paginator
* **`config/urls.py`**  
![Pagination_urls2](https://user-images.githubusercontent.com/17983434/128661929-233cd230-5f84-4b88-9139-db4af84755ea.PNG)

* **`pagination/views.py`**  
![Pagination_Paginator_Views](https://user-images.githubusercontent.com/17983434/128661597-1b9198ad-f116-492e-aeaf-1a301e74fd7a.PNG)

* **서버 구동 후 주소 접근**  
![Pagination_pagination](https://user-images.githubusercontent.com/17983434/128662043-a61b6487-ee27-49e3-86a9-939325c4bcc3.PNG)

### 3. Template를 사용하여 데이터 출력
* **`config/urls.py`**  
![Pagination_urls3](https://user-images.githubusercontent.com/17983434/128662167-b429192c-3598-4277-a379-792e195f2968.PNG)

* **`pagination/views.py`**  
![Pagination_List_Views](https://user-images.githubusercontent.com/17983434/128662623-92f8628c-b7d6-462a-a4eb-f58d5b6f75e2.PNG)

* **`templates/list.html`**  
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <title>페이징 리스트 페이지</title>
</head>

<body style="margin: 30px;">
    <table class="table table-striped">
        <tr>
            <td>번호</td><td>내용</td><td>작성일시</td>
        </tr>
        {% for data in info %}
        <tr>
            <td>{{ data.id }}</td>
            <td>{{ data.text }}</td>
            <td>{{ data.cre_date | date:'Y-m-d H:i:s'}}</td>
        </tr>
        {% endfor %}
    </table>
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전 페이지 -->
        {% if datas.has_previous %}
        <li class="page-item">
            <a class="page-link" href="?page={{ datas.previous_page_number }}">이전</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">이전</a>
        </li>
        {% endif %}
        <!-- 페이지 리스트 -->
        {% for page_number in datas.paginator.page_range %}
        {% if page_number >= datas.number|add:-3 and page_number <= datas.number|add:3 %}
            {% if page_number == datas.number %}
            <li class="page-item active" aria-current="page">
                <a class="page-link" href="?page={{ page_number }}">{{ page_number }}</a>
            </li>
            {% else %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_number }}">{{ page_number }}</a>
            </li>
            {% endif %}
        {% endif %}
        {% endfor %}
        <!-- 다음 페이지 -->
        {% if datas.has_next %}
        <li class="page-item">
            <a class="page-link" href="?page={{ datas.next_page_number }}">다음</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">다음</a>
        </li>
        {% endif %}
    </ul>
    <!-- 페이징처리 끝 -->
</body>

</html>
```

* **`서버 구동 및 마무리`**  
![Pagination_End](https://user-images.githubusercontent.com/17983434/128662817-ca81e78e-aa2f-4fb7-9c74-a07d675ea651.PNG)