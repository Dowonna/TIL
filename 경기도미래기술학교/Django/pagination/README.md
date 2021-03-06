2021-08-09 | μ κ· μμ±

---

## Pagination

### [π **Bootstrap Reference | Pagination**](https://getbootstrap.com/docs/4.4/components/pagination/)

### 1. νμ€νΈμ© λ°μ΄ν° μλ ₯
* **`config/settings.py` λ±λ‘**  
![Pagination_App_Definition](https://user-images.githubusercontent.com/17983434/128659381-c44202f1-8e40-4e37-8c21-38fd4233630f.PNG)

* **`pagination/models.py` μμ±**  
![Pagination_Create_Model](https://user-images.githubusercontent.com/17983434/128659626-bbfab579-c91a-49f0-a72c-fe3e5001f893.PNG)

* **`python manage.py makemigrations & migrate` μ€ν**
    * **μ¬μ© μ€μΈ DBμ λ§κ² μ€μ (<u>MariaDB κΈ°μ€</u>)**  
    ![Pagination_Migrate](https://user-images.githubusercontent.com/17983434/128659900-02a57ff1-ba04-4c2a-a985-260acd4f616d.PNG)

    * **μλμ λ λͺλ Ήμ΄λ₯Ό μ€ν**
    ```plaintext
    $ python manage.py makemigrations
    ```
    ```plaintext
    $ python manage.py migrate
    ```

* **`config/urls.py` μ£Όμ μμ±**  
![Pagination_urls](https://user-images.githubusercontent.com/17983434/128660370-93b9ee61-4002-44dc-8d63-8573f84e50b1.PNG)

* **`pagination/views.py` λ°μ΄ν° μλ ₯ κΈ°λ₯ ν¨μ μμ±**  
![Pagination_views](https://user-images.githubusercontent.com/17983434/128660542-4a032ead-e506-41dc-881e-e5d13d538b4a.PNG)

* **μλ² κ΅¬λ ν DBμ νμ€νΈ λ°μ΄ν° λ±λ‘**
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

* **μλ² κ΅¬λ ν μ£Όμ μ κ·Ό**  
![Pagination_pagination](https://user-images.githubusercontent.com/17983434/128662043-a61b6487-ee27-49e3-86a9-939325c4bcc3.PNG)

### 3. Templateλ₯Ό μ¬μ©νμ¬ λ°μ΄ν° μΆλ ₯
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
    <title>νμ΄μ§ λ¦¬μ€νΈ νμ΄μ§</title>
</head>

<body style="margin: 30px;">
    <table class="table table-striped">
        <tr>
            <td>λ²νΈ</td><td>λ΄μ©</td><td>μμ±μΌμ</td>
        </tr>
        {% for data in info %}
        <tr>
            <td>{{ data.id }}</td>
            <td>{{ data.text }}</td>
            <td>{{ data.cre_date | date:'Y-m-d H:i:s'}}</td>
        </tr>
        {% endfor %}
    </table>
    <!-- νμ΄μ§μ²λ¦¬ μμ -->
    <ul class="pagination justify-content-center">
        <!-- μ΄μ  νμ΄μ§ -->
        {% if datas.has_previous %}
        <li class="page-item">
            <a class="page-link" href="?page={{ datas.previous_page_number }}">μ΄μ </a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">μ΄μ </a>
        </li>
        {% endif %}
        <!-- νμ΄μ§ λ¦¬μ€νΈ -->
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
        <!-- λ€μ νμ΄μ§ -->
        {% if datas.has_next %}
        <li class="page-item">
            <a class="page-link" href="?page={{ datas.next_page_number }}">λ€μ</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">λ€μ</a>
        </li>
        {% endif %}
    </ul>
    <!-- νμ΄μ§μ²λ¦¬ λ -->
</body>

</html>
```

* **`μλ² κ΅¬λ λ° λ§λ¬΄λ¦¬`**  
![Pagination_End](https://user-images.githubusercontent.com/17983434/128662817-ca81e78e-aa2f-4fb7-9c74-a07d675ea651.PNG)