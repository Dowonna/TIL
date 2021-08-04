## 1. JPA 기본 개념

---

JPA는 JDBC와 애플리케이션(Application) 간에 작동하는 ORM(Object-Relational Mapping) 기술 표준을 일컫는다(참고로 ORM은 관계형 DB와 객체를 매핑(Mapping)한다는 의미이다).

![https://blog.kakaocdn.net/dn/beEadC/btqxdQZcueT/Q3vBx9vM7WkhjKOKAlbGC1/img.png](https://blog.kakaocdn.net/dn/beEadC/btqxdQZcueT/Q3vBx9vM7WkhjKOKAlbGC1/img.png)

사진 출처 : [https://sugerent.tistory.com/569](https://sugerent.tistory.com/569)

---

## 2. 왜 사용해야 할까?

---

### 2.1 성능

가장 큰 이유는 API의 응답속도의 개선과 애플리케이션과 DB 사이에서 다양한 방식으로 성능 최적화 기회를 제공한다는 점이다.

그렇다면 어떠한 이점을 가져다주는지 다음 예시를 통해 알아보도록 하자.

```java
String userId = "uniqueId"
User user1 = jpa.find(userId);
User user2 = jpa.find(userId);
```

같은 트랜잭션(Transaction) 안에 같은 유저를 두번 검색할 경우, JDBC의 경우 User를 검색할 때마다 DB와 SELECT를 통해 통신을 두번하는 상황이 발생한다.

하지만 JPA를 사용하면 SQL 구문을 한번만 DB에 전달하고 두번째는 검색한 엔티티(Entity) 객체를 다시 사용한다.

### 2.2 생산성

Java Collection에 객체를 저장하듯 JPA에게도 저장할 객체를 전달하기만 하면 되기에 JDBC를 사용하는 반복 작업을 대신 처리해 준다는 점이다.

```java
jpa.persist(user);             // 저장
User user = jpa.find(userId);  // 검색
```

- CRUD SQL을 직접 작성하지 않아도 됨.
- DDL 구문을 자동으로 생성해 줌.
- DB 설계 중심을 객체 설계 중심으로 중점을 바꿀 수 있음.

### 2.3 벤더 독립성과 데이터 접근 추상화

관계형 DB는 같은 기능이라도 벤더(Vender)마다 사용법이 다르기 때문에 애플리케이션은 처음 선택한 DB 기술에 종속되고 다른 DB로 변경하기 어려워지게 된다.

JPA는 애플리케이션과 DB 간에 추상화된 데이터 접근 계층을 제공하여 특정 DB 기술에 종속되지 않도록 한다.  만약 DB를 변경하고 싶으면 JPA에게 DB 변경을 알리기만 하면 된다. JPA를 사용하면 로컬(Local) 개발환경에서는 H2를 사용하고 사용환경은 Oracle이나 MySQL을 사용할 수 있다.

![https://media.vlpt.us/images/aonee/post/6444a9d1-f68e-4c88-bf44-f5eb4fb1c1c0/image.png](https://media.vlpt.us/images/aonee/post/6444a9d1-f68e-4c88-bf44-f5eb4fb1c1c0/image.png)

사진 출처 : [https://velog.io/@aonee/JPA-기초와-매핑](https://velog.io/@aonee/JPA-%EA%B8%B0%EC%B4%88%EC%99%80-%EB%A7%A4%ED%95%91)

### 2.4 유지보수

SQL을 직접 다루면 엔티티에 필드(Field)를 하나만 추가해도 관련된 등록이나 수정, 검색 SQL과 결과를 매핑하기 위한 JDBC 코드를 모두 변경해야 한다.

이러한 과정을 JPA가 대신 처리해주기 때문에 필드를 추가, 삭제하더라도 수정해야 할 코드가 줄어드는 장점이 있다.

## 2.5 Paradigm 불일치 문제 해결

JPA는 비교나 상속, 객체 그래프 탐색, 연관관계와 같은 불일치 문제를 해결해 준다.

## 3. 영속성 관리

---

### 3.1 영속성 컨텍스트(Persistence Context)

기본 개념으로는 **"**엔티티를 영구 저장하는 환경**"** 으로 보면 된다. EntityManager로 엔티티를 저장하거나 검색하면 엔티티 매니저(Entity Manager)는 영속성 컨텍스트에서 보관하고 관리한다.

persist() 메서드는 엔티티 매니저를 사용해서 유저 엔티티를 영속성 컨텍스트에 저장한다.

### 3.2 엔티티 생명주기(Entity LifeCycle)

엔티티에는 아래와 같은 4가지 상태가 존재한다.

![https://4.bp.blogspot.com/-DVQbYHLNYSQ/WvJvTSK24RI/AAAAAAAAMN8/kyNC3psQCYc00z5DcsYmLF7Qmr0-YqvJwCLcBGAs/s1600/jpa.png](https://4.bp.blogspot.com/-DVQbYHLNYSQ/WvJvTSK24RI/AAAAAAAAMN8/kyNC3psQCYc00z5DcsYmLF7Qmr0-YqvJwCLcBGAs/s1600/jpa.png)

사진 출처 : [https://doublesprogramming.tistory.com/259?category=754820](https://doublesprogramming.tistory.com/259?category=754820)

- 영속(Managed) : 영속성 컨텍스트에 저장되어 있는 상태
- 준영속(Detached) : 영속성 컨텍스트에 저장되었다가 분리된 상태
- 비영속(New / Transient) : 영속성 컨텍스트와 관계 없는 상태
- 삭제(Remove) : 삭제되어 있는 상태

#### 3.2.1 영속

엔티티 매니저를 통해 엔티티를 영속성 컨텍스트에 저장된 상태를 일컫는다. 관리하는 엔티티를 '영속 상태'라고 한다.

```java
// 저장 : 영속
entityManager.persist(user);
// 특정 검색 : 영속
entityManager.find("userId01");
// 목록 검색 : 영속
List<User> users = entityManager
			.createQuery("SELECT u FROM User u", User.class)
			.getResultList();
```

#### 3.2.2 준영속

영속성 컨텍스트가 관리하던 영속 상태의 엔티티를 관리하지 않으면 준영속 상태로 바뀌게 된다. 만약 특정 엔티티를 준영속 상태로 만들고 싶으면 다음의 메서드(Method)를 호출하면 된다.

- entityManager.detach() : 분리
- entityManager.close() : 영속성 컨텍스트를 닫음
- entityManager.clear() : 영속성 컨텍스트를 초기화함

#### 3.2.3 비영속

엔티티 객체를 생성하여 정제되지 않은 순수한 객체의 상태이며 저장하지 않은 상태를 일컫는다. 따라서 영속성 컨텍스트 및 DB와는 관련이 없다.

```java
// 객체 생성 : 비영속
User user = new User();
user.setUserId("userId01");
user.setUserName("kamilLee");
```

#### 3.2.4 삭제

엔티티를 영속성 컨텍스트와 DB에서 삭제한다.

```java
entityManager.remove();
```

## 4. 영속성 컨텍스트의 기본적인 특징

---

기본적인 특징은 다음과 같다.

- 영속성 컨텍스트에 저장된 엔티티는 트랜잭션을 커밋(Commit)하는 순간, 즉시 DB에 반영된다. 이를 '플러시(Flush)'라고 한다.
- 영속성 컨텍스트는 엔티티를 식별자 값으로 구분한다. 즉, 영속 상태는 식별자 값이 존재해야 한다.
- 장점

    1) 트랜잭션을 지원하는 쓰기 지연이 가능함

    2) 변경을 감지함

    3) 지연 로딩(FetchType.LAZY)

    4) 1차 캐시

    5) 동일성을 보장함

영속성 컨텍스트가 필요한 이유를 CRUD를 통해 알아보도록 하자.

### 4.1 검색(find) : 동일성 보장, 1차 캐시

영속 상태의 엔티티는 이곳에 저장된다. 영속성 컨텍스트 내부에는 기본적으로 캐시를 가지고 있는데 이를 1차 캐시라고 한다. 보통 내부에 맵(Map)이 있는데 키(Key)는 @Id 로 매핑한 식별자이며 값은 엔티티 컨텍스트로 사용된다.

```java
User user = new User();
user.setUserId("userId01");
user.setUserName("KamilLee");

/**
* # 기본은 영속 상태이며 캐시는 1차 캐시로 저장된다.
*/
entityManager.persist(user);  // 엔티티를 저장함

/**
* # 만약 1차 캐시에 존재하는 엔티티를 검색할 경우...
* 1) 1차 캐시에서 검색을 진행
* 2) 검색된 값을 반환
*/
User user1 = entityManager.find(User.class, "userId01");  // 특정 ID를 검색함

/**
* # 만약 1차 캐시에 존재하지 않는 엔티티를 검색할 경우...
* 1) 1차 캐시에서 userId02를 식별자로 가진 엔티티를 검색
* 2) 1차 캐시에 존재하지 않기 때문에 DB에서 검색해서 엔티티를 생성
* 3) 1차 캐시에 저장
* 4) 검색된 값을 반환
*/
User user2 = entityManager.find(User.class, "userId02");  // 특정 ID를 검색함

/**
* # 영속 엔티티의 동일성
* : 식별자가 같은 엔티티를 두 번 검색함
*/
User kamil = entityManager.find(User.class, "userId01");
User lee = entityManager.find(User.class, "userId01");

/**
* 엔티티 kamil과 lee는 1차 캐시에 있는
* 같은 엔티티를 받았기 때문에 같은 인스턴스이다.
*/
System.out.println(kamil == lee);  // TRUE
```

### 4.2 등록 : 트랜잭션을 지원하는 쓰기 지연(Transactional Write-behind)

엔티티 매니저는 트랜잭션을 커밋하기 전까지 DB에 엔티티를 저장하지 않고, 내부 쿼리(Query) 저장소에 SQL(INSERT) 구문을 쌓아 둔다. 쓰기 지연은 트랜잭션을 커밋할 때 모아둔 SQL을 DB에 전송하는 것을 일컫는다.

커밋 직후 영속성 컨텍스트는 플러시를 하게 되는데, 영속성 컨텍스트의 변경 사항을 DB에 동기화하는 작업을 일컫는다.

```java
/**
* # userA, userB 객체를 생성
* # 엔티티 매니저 생성, 트랜잭션 획득
*/
transaction.begin();  // 트랜잭션을 개시함

// SQL(INSERT) 구문을 DB에 보내지는 않음
entityManager.persist(userA);
entityManager.persist(userB);

// 커밋 수행 직후 SQL(INSERT) 구문을 DB에 전송함
transaction.commit();  // 트랜잭선을 커밋함
```

## 4.3 수정 : 지연 로딩, 변경 감지

```java
// # 엔티티 매니저 생성, 트랜잭션 획득
transaction.begin();

User findUser = entityManager.find(User.class, "userId01"); // 영속 엔티티를 검색함

// 영속 엔티티 데이터 수정(SQL - UPDATE)
findUser.setUserName("이민재");
findUser.setUserAge(28);

//entityManager.update(findUser);  // 없는 코드를 만들어 내진 말자

transaction.commit();  // 트랜잭션을 커밋함
```

JPA에서는 수정과 관련된 메서드는 따로 존재하지 않으며 위와 같이 엔티티를 검색하고 데이터만 변경해주기만 하면 된다. 이를 '변경 감지'라고 한다.

그렇다면 이 기능의 작동 방식에 대해 알아보자.

JPA는 엔티티를 영속성 컨텍스트에 보관할 때, 최초 상태를 복사해 저장해두는데 이를 스냅샷(Snapshot)이라고 한다. 그리고 플러시되는 시점에 스냅샷과 엔티티를 비교하여 변경된 엔티티를 찾게 된다.

1) 트랜잭션 커밋 → 플러시를 호출함

2) 엔티티와 스냅샷 비교 → 변경된 엔티티를 찾음

3) 변경된 엔티티가 존재하면 수정 쿼리를 생성 → 쓰기 지연 SQL 저장소에 보관함

4) 쓰기 지연 SQL을 DB에 전송함

5) DB 트랜잭션을 커밋함

변경 감지는 영속성 컨텍스트가 관리하는 영속 상태의 엔티티에만 적용되고, 비영속, 준영속 상태의 엔티티는 적용되지 않는다.

변경 감지로 인해 생성된 SQL(UPDATE) 구문은 엔티티의 모든 필드를 업데이트한다. 모든 필드를 DB에 보내면 데이터 전송량이 증가하는 단점이 존재하나 다음과 같은 장점을 얻을 수 있다.

- DB에 동일한 쿼리를 보내면 DB는 이전에 한번 파싱(Parsing)된 쿼리를 재사용할 수 있음.
- 모든 필드를 사용하면 수정된 쿼리는 항상 같음. 그리고 애플리케이션 로딩 시점에 수정 쿼리를 미리 생성하고 이를 재사용할 수 있음.

### 4.4 삭제

엔티티를 삭제하려면 대상 엔티티를 검색하고 엔티티 매니저에 대상 엔티티를 건네주면 해당 엔티티를 삭제한다. 엔티티 등록과 동일하게 삭제 쿼리를 쓰기 지연 SQL 저장소에 등록한 후 트랜잭션을 커밋해 플러시를 호출하면 DB에 삭제 쿼리를 전달한다.

```java
User user1 = entityManager.find(User.class, "userId01");  // 삭제 대상 엔티티를 검색함
entityManager.remove(user1); // 대상 엔티티를 삭제함
```

## 5. 플러시(Flush)

플러시는 영속성 컨텍스트의 변경 내용을 DB에 반영한다. 이를 실행하면 다음과 같은 일이 발생한다.

1) 변경 감지가 동작해서 영속성 컨텍스트에 있는 모든 엔티티를 스냅샷과 비교해서 수정된 엔티티를 찾는다. 수정된 엔티티는 수정 쿼리를 만들어 쓰기 지연 SQL 저장소에 등록한다.

2) 쓰기 지연 SQL 저장소의 쿼리를 DB에 전송한다.

영속성 컨텍스트를 플러시하는 방법은 아래와 같이 3가지 방법이 있다.

### 5.1 JPQL 쿼리 실행시 플러시 자동 호출

```java
/**
* # 객체 userA, userB, userC 생성
* # 엔티티 매니저 생성, 트랜잭션 획득
*/
entityManager.persist(userA);  // userA 등록
entityManager.persist(userB);  // userB 등록
entityManager.persist(userC);  // userC 등록

// JPQL 실행
List<User> users = entityManager.createQuery("SELECT u FROM User u", User.class)
			.getResultList();

transaction.commit();  // 트랜잭션을 커밋함
```

JPQL와 같은 객체지향 쿼리를 호출할 때에도 플러시가 실행된다. persist() 메서드를 호출해서 엔티티 userA, userB, userC 를 영속 상태로 만들고, 영속성 컨텍스트에 있지만 아직 DB에는 반영되지 않았다. 이때 JPQL을 실행하면 SQL로 변환되어 DB에서 엔티티에서 검색한다. 그런데 userA, userB, userC 는 아직 DB에 없어서 쿼리 결과로 검색되지 않는다. 따라서 쿼리를 실행하기 직전에 영속성 컨텍스트를 플러시해서 변경 내용을 DB에 반영해야만 한다.

JPA는 이런 문제를 예방하기 위해 JPQL을 실행할 때에도 플러시를 자동으로 호출한다. 그래서 userA, userB, userC 들도 쿼리 결과에 포함된다.

find() 메서드의 경우는 플러시가 실행되지 않는다.

플러시는 영속성 컨텍스트에 보관된 엔티티를 삭제하는 것이 아니라 영속성 컨텍스트의 내용 변경을 DB에 동기화하는 것이다.

### 5.2 트랜잭션 커밋 시 플러시 자동 호출

DB에 변경 내용을 SQL로 직접 전달하지 않고 트랜잭션만 커밋하면 어떤 데이터도 DB에 반영되지 않는다. 그래서 트랜잭션을 커밋하기 전에 플러시를 호출해서 영속성 컨텍스트의 변경 내용을 DB에 반영해야 한다. JPA는 이런 문제를 사전에 예방하기 위해 트랜잭션을 커밋할 때 플러시를 자동으로 호출한다.

### 5.3 직접 호출

entityManager.flush() 메서드를 직접 호출해서 영속성 컨텍스트를 강제로 플러시하는 방법이다. 혹여 다른 프레임워크(FrameWork)와 함께 사용하고 싶다면 JPA를 사용하는 용도 외에는 거의 사용하지 않는다.

## 6. 준영속

영속성 컨텍스트가 관리하는 영속 상태의 엔티티가 영속성 컨텍스트에서 분리된 것을 준영속 상태라고 한다. 준영속 상태의 엔티티는 영속성 컨텍스트가 제공하는 기능을 사용할 수 없는 제약이 있다.

### 6.1 엔티티를 준영속 상태로 전환 : detach()

detach() 메서드는 특정 엔티티를 준영속 상태로 만드는데 다음의 코드를 보면 먼저 유저(User) 엔티티를 영속화한 다음 detach() 메서드를 호출했다. 이 메서드를 호출하면 1차 캐시, 쓰기 지연 SQL 저장소까지 해당 엔티티를 관리하기 위한 정보가 모두 삭제된다.

```java
// 영속 상태
entityManager.persist(user);

// 유저 엔티티를 영속성 컨텍스트에서 분리 -> 준영속 상태
entityManager.detach(user);

transaction.commit();  // 트랜잭션을 커밋함
```

### 6.2 영속성 컨텍스트 초기화 : clear()

clear() 메서드는 영속성 컨텍스트를 초기화해서 해당 영속성 컨텍스트의 모든 엔티티를 준영속 상태로 만든다. 영속성 컨텍스트를 삭제하고 새로 작성하는 것과 같다.

```java
// 엔티티 조회, 영속 상태
User user = entityManager.find(User.class, "userId01");

// 영속성 컨텍스트 초기화
entityManager.clear();

// -> 준영속 상태
user.setUserAge(18);  // 변경 감지는 준영속 상태이기 때문에 변경되지 않음
```

### 6.3 영속성 컨텍스트 종료 : close()

영속성 컨텍스트를 종료하면 해당 영속성 컨텍스트가 관리하던 영속 상태의 엔티티가 모두 준영속 상태가 된다.

```java
// 엔티티 매니저 생성, 트랜잭션 획득
transaction.begin(); // 트랜잭션을 개시함

User userA = entityManager.find(User.class, "userId01");
User userB = entityManager.find(User.class, "userId02");

transaction.commit();  // 트랜잭션을 커밋함

entityManager.close();  // 영속성 컨텍스트를 닫음
```

### 6.4 준영속 상태의 특징

준영속 상태의 엔티티의 특징은 다음과 같다.

- 비영속 상태는 식별지값이 없지만 준영속 상태는 이미 영속 상태였기 때문에 식별자 값을 가지고 있음
- 지연 로딩을 할 수 없음
- 거의 비영속 상태에 가깝기 때문에 영속성 컨텍스트가 제공하는 어떠한 기능도 동작하지 않음

### 6.5 병합 : merge()

준영속 상태의 엔티티를 다시 영속 상태로 변경하려면 병합(Merge)을 사용하면 된다. merge() 메서드는 준영속 상태의 엔티티를 받아서 해당 정보를 새로운 영속 상태의 엔티티를 반환한다.

```java
public class ExampleMergin {

	// 엔티티 매니저 팩토리 생성
	private static EntityManageFactory emf = Persistence.createEntityManagerFactory("jpaTest");

	public static void main(String[] args) {
			// 유저 엔티티를 생성 -> 준영속 상태
			User user = createUser("userId01", "KamilLee", 28);
			// 준영속 상태 -> 유저 정보 변경 : 변경 불가
			user.setUserName("이민재");
			// 유저 엔티티를 병합함
			mergeUser(user);
	}

	// 유저 엔티티 생성 -> 영속성 컨텍스트 종료
	private static User createUser(String id, String userName, int age) {
			// 엔티티 매니저를 생성함
			EntityManager em1 = emf.createEntityManager();
			// 트랜잭션을 획득함
			EntityTransaction tx1 = em1.getTransaction();
			tx1.begin();  // 트랜잭션을 개시함

			// 유저 객체를 생성함
			User user = new User();
			user.setUserId(uid);
			user.setUserName(userName);
			user.setUserAge(Age);

			// 유저 엔티티를 등록함
			em1.persist(user);
			tx1.commit();  // 트랜잭션을 커밋함

			em1.close();  // 영속성 컨텍스트를 닫음 -> 유저 엔티티를 준영속 상태로 변경됨

			return user;
	}

	// 병합
	private static void mergeUser(User user) {
			// 엔티티 매니저를 생성함
			EntityManager em2 = emf.createEntityManager();
			// 트랜잭션을 획득함
			EntityTransaction tx2 = em2.getTransaction();
			tx2.begin();  // 트랜잭션을 개시함

			// 유저 엔티티를 병합함 -> 유저 엔티티의 변경을 감지함 -> DB에 반영함
			User mergeUser = em2.merge(user);
			tx2.commit();  // 트랜잭션을 커밋함

			System.out.println("user = " + user.getUserName());
			System.out.println("mergeUser = " + mergeUser.getUserName());
			System.out.println("em2 contains user = " + em2.contains(user));
			System.out.println("em2 contains mergeUser = " + em2.contains(mergeUser));

			em2.close();
	}
}
```

흐름은 다음과 같다.

1) createUser() 메서드에서 유저 엔티티를 생성하고, 등록한 후에 영속성 컨텍스트를 종료시켜 준영속 상태로 만듬

2) 준영속 상태의 유저 엔티티를 변경하면 변경사항이 적용되지 않음

3) mergeUser() 메서드에서 유저 엔티티를 병합하고, 변경사항을 감지하여 DB에 이를 동기화함

4) 반환된 mergeUser와 user가 영속성 컨텍스트에 존재하는지 contains() 메서드를 통해 확인함

다음은 출력된 결과물이다.

```
Hibernate:
		/*insert com.KamilLee.jpaTest.User
				/* insert
				into
						USER
						(AGE, NAME, ID)
				values
						(?, ?, ?)
Hibernate:
		/* load com.KamilLee.jpaTest.User */ select
				user0_.ID as ID1_0_0_,
				user0_.AGE as AGE2_0_0_,
				user0_.NAME as NAME3_0_0_
		from
				USER user0_
		where
				user0_.ID=?
Hibernate:
		/* update
				com.KamilLee.jpaTest.User */ update
						USER
				set
						AGE=?,
						NAME=?
				where
						ID=?
user = 이민재
mergeUser = 이민재
em2 contains user = false
em2 contains mergeUser = true
```

이를 통해 확인할 수 있는 것은 merge() 메서드를 통해 반환받은 mergeUser와 user는 다른 인스턴스라는 것을 알 수 있으며, mergeUser는 영속 상태이고, user는 여전히 준영속 상태라는 것을 알 수 있다. 이렇게 준영속 엔티티를 참조하던 변수는 영속 엔티티를 참조하도록 변경하는 것이 바람직하며 보다 안전하다고 할 수 있다.

```java
//User mergeUser = em2.merge(user); 코드를 변경
user = em2.merg2(user);  // 참조를 변경
```

merge() 메서드는 비영속 엔티티도 영속 상태로 만들 수도 있다.

```java
User user = new User();  // 비영속 상태
User newUser = entityManager.merge(user);  // 엔티티 병합
```

병합은 파라미터로 넘어온 엔티티의 식별자로 영속성 컨텍스트를 검색하고 결과가 없을 경우 DB를 검색한다. 만약 DB에도 존재하지 않는다면 새로운 엔티티를 생성해 병합을 시행하게 된다. 그리고 준영속, 비영속을 가리지 않는다는 특징이 있다.

## 7. 엔티티 매핑

---

JPA를 사용할 떄에는 엔티티와 테이블(Table)을 정확히 매핑하는 것이 가장 중요하다. JPA는 매핑 어노테이션(Annotation)을 지원하는데 다음과 같이 분류할 수 있다.

- 객체와 테이블 간 매핑
- 기본키(Primary Key) 매핑
- 연관관계 매핑
- 필드와 컬럼(Column) 매핑

### 7.1 @Entity

JPA를 사용해서 테이블과 매핑할 클래스에는 @Entity 어노테이션을 붙인다. @Entity가 붙은 클래스는 JPA과 관리하는 것으로 엔티티라고 부른다.

#### 7.1.1 속성

- name : JPA와 사용할 엔티티의 이름을 지정, 사용하지 않을 경우, 클래스 이름이 적용(예시 : name = "UserTest")

#### 7.1.2 주의사항

- 저장할 필드에는 final을 사용할 수 없음
- 기본생성자가 필수로 들어가야 됨
- final, enum, interface, inner 클래스는 사용할 수 없음

### 7.2 @Table

@Table 어노테이션은 엔티티와 매핑할 테이블을 지정하고, 이를 생략시 매핑한 엔티티 이름을 테이블 이름으로 사용한다.

#### 7.2.1 속성

- name : 매핑할 테이블의 이름
- catalog : catalog 기능이 있는 DB에서 catalog를 매핑
- schema : schema 기능이 있는 DB에서 schema를 매핑
- uniqueConstraint : DDL(Data Definition Language) 매핑 시에 유니크(Unique) 제약조건을 만든다. 스키마 자동생성 기능을 사용해서 DDL을 만들 때만 사용

### 7.3 DB 스키마 자동생성

JPA는 DB 스키마를 자동으로 생성하는 기능을 제공한다. 클래스의 매핑정보를 보면 어떤 테이블에 어떤 컬럼을 사용하는지 알 수 있다. 다음은 예제에 사용할 클래스를 작성한 것이다.

#### 7.3.1 스키마 자동생성을 위한 클래스 작성

```java
@Entity  // 클래스와 테이블을 매핑함
@Table(name = "USERTEST")  // 매핑할 테이블 정보를 명시함
public class User {
		@Id  // 기본키 매핑
		@Column(name = "ID")  // 필드를 컬럼에 매핑함
		private String userId;
		@Column(name = "NAME")
		private String userName;
		@Column(name = "AGE")
		private Integer userAge;

		// 유저 타입 구분
		@Enumerated(EnumType.String)
		private RoleType roleType;
		// 날짜 타입 매핑
		@Temporal(TemporalType.TIMESTAMP)
		private Date createdDate;
		// 날짜 타입 매핑
		@Temporal(TemporalType.TIMESTAMP)
		private Date lastModifiedDate;
		@Lob  // 길이 제한 없게 해주는 어노테이션
		private String description;
		
		// Getter, Setter, toString...
}
```

#### 7.3.2 스키마 자동생성 옵션 설정

persistence.xml에서 다음과 같은 속성을 추가하면 DB 테이블을 자동으로 생성해주고, 콘솔(Console)에 DDL을 출력해 준다.

```xml
<property name="hibernate.hbm2ddl.auto" value="create" />
<property name="hibernate.show_sql" value="true" />
```

프로젝트를 실행 후 콘솔 화면을 확인해 보면 다음과 같이 DDL이 출력되고, DB에 테이블이 생성되는 것을 확인할 수 있다.

```
Hibernate:
		drop table USER if exists
Hibernate:
		create table USER (
				ID varchar2(255) not null,
				AGE integer,
				createdDate timestamp,
				description clob,
				roleType varchar2(255)
				NAME varchar2(255)
				lastModifiedDate timestamp,
				primary key (ID)
		)
```

스키마 자동생성 기능을 사용하면 애플리케이션 실행 시점에 DB 데이블을 자동으로 생성된다. 단 스키마 자동생성 기능이 만든 DDL은 완벽하지 않기 때문에 개발환경에서 사용하는 등 참고 정도로만 사용하도록 하자.

[hibernate.hbm2ddl.auto](http://hibernate.hbm2ddl.auto)의 속성은 다음과 같다.

- create : 기존의 테이블을 삭제하고 새로운 테이블을 생성함**(DROP + CREATE)**
- create-only : DB를 새로 생성함**(CREATE)**
- create-drop : 애플리케이션을 종료할 때 생성한 DDL을 삭제함**(DROP + CREATE + DROP)**
- drop : DB를 드롭함**(DROP)**
- validate : DB 테이블과 엔티티 매핑정보를 비교해서 차이가 있으면 경고 메시지와 함께 해당 애플리케이션을 실행하지 않음
- update : DB 테이블과 엔티티 매핑정보를 비교해서 변경사항만 수정함
- none : 자동생성 기능을 사용하지 않으려면 속성을 삭제하거나, 유효하지 않은 값을 주면 됨

그리고 HBM2DDL에서 주의할 점은 DDL을 수정하는 옵션(create, create-drop, update)은 오직 개발단계에서만 사용해야만 한다. 객체 관계 매핑 작업을 수행하기 전의 개발 초기 단계 혹은 프로토타입 제작을 목표로 하지 않는 이상은 말이다. 도메인(Domain) 설정에서 데이터 저장 공간의 길이를 지정하지 않을 수도 있으며 Not Null 등의 제약조건을 빠뜨릴 수 있기 때문에 실수하기도 더 쉽고 오류를 찾기도 일반적인 SQL DDL 문보다 복잡하기 때문이다.

- 개발 초기 단계 : create, update
- 테스트 서버 : update, validate
- 스테이징, 운영서버 : validate, none

참고로 JPA 2.1 버전부터는 스키마 자동생성 기능을 표준으로 지원하지만 HBM2DDL 속성이 지원하는 update, validate 옵션을 지원하지 않는다.

### 7.3.3 이름 매핑 전략 변경

보통 단어와 단어를 구분할 때 Java는 카멜표기법(Camel Case)을 DB는 언더스코어(UnderScore)를 주로 사용한다. 이러한 차이를 매핑하기 위해 @Column.name 속성을 명시적으로 사용해서 이름을 지정해 줄 필요가 있다.

```java
@Column(name = "role_type")
String roleType;
```

이름 매핑 전략을 직접 지정해줘도 되지만, persistence.xml에서 같이 아래와 같이 속성을 지정해주면 자동으로 Java의 카멜표기법을 테이블의 언더스코어 표기법으로 이를 매핑한다.

```xml
<property name="hibernate.ejb.naming_strategy" value="org.hibernate.cfg.ImprovedNamingStrategy" />
```

프로젝트를 다시 실행해보면 다음과 같이 카멜표기법에서 언더스코어 표기법으로 컬럼이 매핑된 것을 확인할 수 있다.

```
Hibernate:
		drop table user if exists
Hibernate:
		create table user (
				id varchar2(255) not null,
				age integer,
				created_date timestamp,
				description clob,
				user_type varchar2(255)
				name varchar2(255)
				last_modified_date timestamp,
				primary key (id)
		)
```

### 7.4 DDL 생성기능

유저 클래스에서 유저 이름이 필수로 입력되고, 10자를 초과하지 못하도록 제약조건을 추가해보자.

```java
/**
* # 필수로 입력(null 허용 안함)
* # 길이는 10자로 제한함
*/
@Column(name = "NAME", nullable = false, length = 10)
private String userName;
```

프로젝트를 다시 실행해 보면 제약조건이 다음과 같이 추가되었음을 확인할 수 있다.

```
Hibernate:
		drop table user if exists
Hibernate:
		create table user (
				id varchar2(255) not null,
				age integer,
				created_date timestamp,
				description clob,
				user_type varchar2(255)
				name varchar2(10) not null,  // 제약조건에 의해 컬럼 업데이트
				last_modified_date timestamp,
				primary key (id)
		)
```

다음으로 유니크 제약조건을 만들어주는 @Table의 uniqueConstraints 속성에 대해 알아보자.

유저 클래스에서 테이블 어노테이션에 다음과 같이 유니크 제약조건(유일한 값만 저장함)을 추가해줄 수 있다.

```java
@Entity
// 유니크 제약조건 추가
@Table(name = "USER", uniqueConstraints = {@UniqueConstraint(
				name = "NAME_AGE_UNIQUE",
				columnNames = {"NAME", "AGE"} )})
public class User {

		// ...
}
```

프로젝트를 다시 실행해 보면 제약조건이 다음과 같이 추가되었음을 확인할 수 있다.

```
Hibernate:
		drop table user if exists
Hibernate:
		create table user (
				id varchar2(255) not null,
				age integer,
				created_date timestamp,
				description clob,
				user_type varchar2(255)
				name varchar2(10) not null,
				last_modified_date timestamp,
				primary key (id)
		)
Hibernate:
		alter table user
				add constraint NAME_AGE_UNIQUE unique (name, age)  // 유니크 제약조건 추가
```

## 8. 기본키 매핑

---

기본키 매핑의 경우 '직접 할당'할 수도 있으며 DB가 생성해주는 값을 사용할 수도 있다. **DB마다 기본키를 생성하는 방식이 다르기 때문에 JPA가 제공하는 DB 기본키 생성 전략은 다음과 같이 다양하다.

1) 직접 할당 : 기본키를 애플리케이션에서 직접 할당함

2) 자동생성 : 대리키(Foreign Key) 사용방식

- IDENTITY : 기본키 생성을 DB에 위임함 - **DB에 의존**
- TABLE : 키 생성 테이블을 사용함 - **DB에 의존하지 않음**
- SEQUENCE : DB 시퀀스를 사용해 기본키를 할당함 - **DB에 의존**
- AUTO : 자동으로 기본키를 생성함

### 8.1 기본키 생성 전략 설정

사용하기 위해서는 persistence.xml에 다음과 같이 속성을 추가할 필요가 있다.

```xml
<property name="hibernate.id.new_generator_mappings" value="true" />
```

### 8.2 직접 할당

직접 할당하기 위해서는 다음과 같이 클래스 필드를 @Id로 매핑하고, 엔티티를 저장하기 전에 애플리케이션에서 기본키를 직접 할당해주면 된다.

```java
// 기본키 직접 할당 전략
@Entity
@Table(name = "USER_DIRECT")
public class UserDirect {
		@Id  // 기본키 매핑
		@Column(name = "ID")
		private String userId;
		@Column(name = "NAME")
		private String userName;

		// gettet, setter, ...
}
```

```java
// 기본키 직접 할당 사용 코드
for(int i = 0; i < 5; i++) {
		UserDirect user = new UserDirect();
		user.setUserName("KamilLee" + i);
		user.setUserId("userId00" + i);  // 기본키 직접 할당
		entityManager.persist(user);
		System.out.println("DIRECT user id = " + user.getUserId());
}
```

코드를 실행한 결과를 출력한 후 확인해보면 다음과 같은 결과를 확인할 수 있다.

```
// 테이블 생성
Hibernate:
		drop table user_direct if exists
Hibernate:
		create table user_direct (
				id varchar2(255) not null,
				name varchar2(255),
				primary key (id)
		)

// 식별자 출력
DIRECT user id = userId00
DIRECT user id = userId01
DIRECT user id = userId02

// 엔티티 DB 테이블 저장
Hibernate:
		insert
		into
				user_direct
				(name, id)
		values
				(?, ?)
Hibernate:
		insert
		into
				user_direct
				(name, id)
		values
				(?, ?)
Hibernate:
		insert
		into
				user_direct
				(name, id)
		values
				(?, ?)
```

@Id에 적용 가능한 Java 타입은 다음과 같다.

- String
- 래퍼(Wrapper)형
- Java 기본형
- java.sql.Date
- java.util.Date
- java.math.BigInteger
- java.math.BigDecimal

### 8.3 IDENTITY 전략

기본키 생성을 DB에 위임하는 방식으로 주로 PostgreSQL, MySQL, DB2에서 사용한다.

유저 클래스를 다음과 같이 작성하고 id 컬럼값을 지정하지 않고 저장하면 콘솔창에서 확인할 수 있듯이 자동으로 기본키가 생성되는 것을 알 수 있다.

```java
// 기본키 IDENTITY 전략
@Entity
@Table(name = "USER_IDENTITY")
public class UserIdentity {
		@Id  // 기본키 매핑
		@GeneratedValue(strategy = GenerationType.IDENTITY)
		private Long userId;
		@Column(name = "NAME")
		private String userName;

		// gettet, setter, ...
}
```

```java
// 기본키 IDENTITY 전략 사용 코드
for(int i = 0; i < 3; i++) {
		UserIdentity user2 = new UserIdentity();
		user2.setUserName("KamilLee" + i);
		// 기본키를 직접 할당하는 코드를 작성할 필요가 없음
		entityManager.persist(user2);
		System.out.println("IDENTITY user id = " + user2.getUserId());
}
```

```
// 테이블 생성
Hibernate:
		drop table user_identity if exists
Hibernate:
		create table user_identity (
				id bigint generated by default as identity,  // 기본키 IDENTITY 생성 전략
				name varchar2(255),
				primary key (id)
		)

// 엔티티 DB 테이블 저장
Hibernate:
		insert
		into
				user_identity
				(id, name)
		values
				(null, ?)
// 식별자 출력
IDENTITY user id = 1

// 엔티티 DB 테이블 저장
Hibernate:
		insert
		into
				user_identity
				(id, name)
		values
				(null, ?)
// 식별자 출력
IDENTITY user id = 2

// 엔티티 DB 테이블 저장
Hibernate:
		insert
		into
				user_identity
				(id, name)
		values
				(null, ?)
// 식별자 출력
IDENTITY user id = 3
```

앞서 기본키를  직접 할당했을 때와 차이점을 확인할 수 있다. 기본키를 직접 할당 했을 때에는 엔티티의 식별자가 바로 출력되었지만, IDENTITY 전략을 사용한 경우 엔티티를 DB에 저장하고 출력된 것을 알 수 있다.

- entityManager.persist()를 호출하는 즉시 SQL(INSERT) 구문이 DB에 바로 전달되기 때문에 트랜잭션을 지원하는 쓰기 지연 기능이 동작하지 않음
- 엔티티가 영속 상태가 되려면 식별자가 반드시 필요한데, IDENTITY 전략의 경우 엔티티를 DB에 저장하지 않으면 식별자를 구할 수 없음

### 8.4 TABLE 전략

키 생성 전용 테이블을 추가로 만들고 여기에 이름과 값을 사용할 컬럼을 만들어 DB 시퀀스를 모방하는 전략으로 이는 모든 DB에서 사용이 가능하다.

```java
// 기본키 TABLE 전략
@Entity
@TableGenerator(name = "USER_SEQ_GENERATOR"), // 식별자 생성기 이름
				table = "TEST_SEQUENCES",  // 키 생성 테이블 이름
				pkColumnValue = "USER_SEQ",  // 키로 사용할 값의 이름
				allocationSize = 1)  // 시퀀스를 한번 호출 시 증가하는 수
public class UserTable {
		@Id  // 기본키 매핑
		@GeneratedValue(strategy = GenerationType.TABLE, generator = "USER_SEQ_GENERATOR")
		private Long userId;

		// ...
}
```

먼저 @TableGenerator를 사용하여 USER_SEQ_GENERATOR라는 이름을 가진 테이블 키 생성기를 등록한다. TEST_SEQUENCCES라는 테이블을 키 생성 테이블로 매핑하고, 키로 사용할 값의 이름을 USER_SEQ_GENERATOR라고 지정했다. 그리고 기본키를 매핑한 곳에 테이블 전략을 사용한다고 명시하고, 키 생성기는 USER_SEQ_GENERATOR으로 지정했다.

```java
// 기본키 TABLE 전략 사용 코드
for(int i = 0; i < 3; i++) {
		UserTable user3 = new UserTable();
		user3.setUserName("KamilLee" + i);
		// 기본키를 직접 할당하는 코드를 작성할 필요가 없음
		entityManager.persist(user3);
		System.out.println("TABLE user id = " + user3.getUserId());
}
```

TABLE 전략은 시퀀스 대신에 테이블을 사용한다는 것만 제외하면 기본적인 틀은 시퀀스 전략과 내부 동작 방식이 동일하다. 그리고 값을 검색하면서 SELECT 쿼리를 사용하고, 다음 값을 증가시키기 위해 UPDATE 쿼리를 사용한다.

```
// 유저 테이블 및 시퀀스 테이블 생성
Hibernate:
		drop table user_table if exists
Hibernate:
		drop table TEST_SEQUENCES if exists
Hibernate:
		create table user_table (
				id bigint not null,
				name varchar2(255),
				primary key (id)
		)
Hibernate:
		create table TEST_SEQUENCES (
				sequence_name varchar2(255) not null,
				next_val bigint,
				primary key (sequence_name)
		)

// 값 검색
Hibernate:
		select
				tbl.next_val
		from
				TEST_SEQUENCES tbl
		where
				tbl.sequence_name=? for update

// 테이블에 값이 존재하지 않을 경우 삽입함
Hibernate:
		insert
		into
				TEST_SEQUENCES
				(sequence_name, next_val)
		values
				(?, ?)

// 다음 값을 증가하기 위해 업데이트함
Hibernate:
		update
				TEST_SEQUENCES
		set
				next_val=?
		where
				next_val=?
				and sequence_name=?
TABLE user id = 1

// 값 검색
Hibernate:
		select
				tbl.next_val
		from
				TEST_SEQUENCES tbl
		where
				tbl.sequence_name=? for update

// 테이블에 값이 존재하지 않을 경우 삽입함
Hibernate:
		insert
		into
				TEST_SEQUENCES
				(sequence_name, next_val)
		values
				(?, ?)

// 다음 값을 증가하기 위해 업데이트함
Hibernate:
		update
				TEST_SEQUENCES
		set
				next_val=?
		where
				next_val=?
				and sequence_name=?
TABLE user id = 2

// 값 검색
Hibernate:
		select
				tbl.next_val
		from
				TEST_SEQUENCES tbl
		where
				tbl.sequence_name=? for update

// 테이블에 값이 존재하지 않을 경우 삽입함
Hibernate:
		insert
		into
				TEST_SEQUENCES
				(sequence_name, next_val)
		values
				(?, ?)

// 다음 값을 증가하기 위해 업데이트함
Hibernate:
		update
				TEST_SEQUENCES
		set
				next_val=?
		where
				next_val=?
				and sequence_name=?
TABLE user id = 3

// 엔티티를 DB에 저장함
Hibernate:
		insert
		into
				user_table
				(name, id)
		values
				(?, ?)
Hibernate:
		insert
		into
				user_table
				(name, id)
		values
				(?, ?)
Hibernate:
		insert
		into
				user_table
				(name, id)
		values
				(?, ?)
```

### 8.5 SEQUENCES 전략

유일한 값을 순서대로 생성하는 특별한 기능을 가진 DB 오브젝트(Object)이다. 시퀀스를 지원하는 DB는 Oracle, DB2, H2, PostgreSQL에서 사용 가능하다.

```java
// SEQUENCE 전략
@Entity
@SequenceGenerator(
				name = "USER_SEQ_GENERATOR"), // 식별자 생성기 이름
				sequenceName = "USER_SEQ",  // 매핑할 DB 시퀀스 이름
				initialValue = 1,  // DDL 생성 시에 사용함
				allocationSize = 1)  // 시퀀스를 한번 호출 시 증가하는 수
public class UserSequence {
		@Id  // 기본키 매핑
		@GeneratedValue(strategy = GenerationType.TABLE, generator = "USER_SEQ_GENERATOR")
		private Long userId;

		// ...
}
```

먼저 사용할 DB의 시퀀스를 매핑해줘야 하는데 @SequenceGenerator를 사용해서 USER_SEQ_GENERATOR라는 시퀀스 생성기를 등록했다. sequenceName 속성으로 USER_SEQ을 지정했는데 JPA는 이 시퀀스 생성기를 실제 DB의 USER_SEQ와 매핑한다.

그리고 키 생성 전략을 GenerationType.SEQUENCE로 설정하고 generator = "USER_SEQ_GENERATOR"로 방금 등록한 시퀀스 생성기를 선택한다. 이렇게 되면 id 식별자 값은 USER_SEQ_GENERATOR 시퀀스 생성기가 할당한다. 

```java
// 시퀀스 사용 코드
for(int i = 0; i < 3; i++) {
		UserSequence user4 = new UserSequence();
		user4.setUserName("kamillee" + i);
		entityManager.persist(user4);
		System.out.println("SEQUENCE user id = " + user4.getUserId());
}
```

코드를 실행하면 다음과 같은 콘솔화면을 볼 수 있다. 출력된 내용을 보면 유저 테이블과 시퀀스를 생성하고 유저객체를 생성하고 저장할 때마다 시퀀스를 호출해 1씩 증가시키는 것을 알 수 있다. IDENTITY 전략과는 다르게 쓰기 지연이 가능한 것도 확인할 수 있다.

```
// 시퀀스 테이블 생성
Hibernate:
		drop table user_sequence if exists
Hibernate:
		drop sequence if exists USER_SEQ
Hibernate:
		create table user_sequence (
				id bigint not null,
				name varchar2(255),
				primary key (id)
		)

// 시퀀스 생성
Hibernate:
		create sequence USER_SEQ start with 1 increment by 1

// 시퀀스 호출 시 값을 1씩 증가시킴
Hibernate:
		call next value for USER_SEQ

// 기본키에 시퀀스 할당
SEQUENCE user id = 1

// 시퀀스 호출 시 값을 1씩 증가시킴
Hibernate:
		call next value for USER_SEQ

// 기본키에 시퀀스 할당
SEQUENCE user id = 2

// 시퀀스 호출 시 값을 1씩 증가시킴
Hibernate:
		call next value for USER_SEQ

// 기본키에 시퀀스 할당
SEQUENCE user id = 3

// 엔티티를 DB에 저장
Hibernate:
		insert
		into
				user_sequence
				(name, id)
		values
				(?, ?)
Hibernate:
		insert
		into
				user_sequence
				(name, id)
		values
				(?, ?)
Hibernate:
		insert
		into
				user_sequence
				(name, id)
		values
				(?, ?)

```

@SequenceGenerator의 속성을 정리해보면 다음과 같다.

- name : 식별자 생성기의 이름
- sequenceName : DB에 등록된 시퀀스의 이름 - **기본값은 hibernate_sequence**
- allocationSize : 시퀀스 호출에 증가하는 수 - **기본값은 50**
- catalog, schema : DB의 catalog, schema 이름
- initialValue : DDL 생성시에만 사용되는 속성이며, 시퀀스 DDL을 생성할 때 처음 시작하는 수를 지정 - **기본값은 1**

사용코드는 IDENTITY 전략과 다를바 없지만 동작방식은 다르다. SEQUENCE 전략이 이루어지는 과정은 다음과 같다.

1) 트랜잭션을 커밋해서 플러시가 일어나면 엔티티를 저장함

2) 조회한 식별자를 엔티티에 할당한 후 영속성 컨텍스트에 이를 저장함

3) entityManager.persist()를 호출할 때 먼저 DB 시퀀스를 사용해 식별자를 검색함

### 8.6 AUTO 전략

DB의 방언(Dialect)에 따라 TABLE, SEQUENCE, IDENTITY 전략 중 자동으로 하나를 선택한다.

```java
// 기본키 AUTO 전략
@Entity
@Table(name = "USER_AUTO")
public class UserAuto {
		@Id  // 기본키 매핑
		@GeneratedValue(strategy = GenerationType.AUTO)
		private Long userId;

		// ...
}
```

```java
// H2 DB 기준 : 기본키 Auto 전략 사용 코드
for(int i = 0; i < 3; i++) {
		UserAuto user5 = new UserAuto();
		user5.setUserName("kamillee" + i);
		entityManager.persist(user5);
		System.out.println("AUTO user id = " + user5.getUserId());
}
```

코드를 실행하면 다음과 같이 출력되는 것을 확인할 수 있다.

```
// AUTO 테이블 생성
Hibernate:
		drop table user_auto if exists
Hibernate:
		drop sequence if exists hibernate_sequence
Hibernate:
		create table user_auto (
				id bigint not null,
				name varchar2(255),
				primary key (id)
		)

// 시퀀스 생성
Hibernate:
		create sequence hibernate_sequence start with 1 increment by 1

// 시퀀스 호출 시 값을 1씩 증가시킴
Hibernate:
		call next value for hibernate_sequence

// 기본키에 시퀀스 할당
AUTO user id = 1

// 시퀀스 호출 시 값을 1씩 증가시킴
Hibernate:
		call next value for hibernate_sequence

// 기본키에 시퀀스 할당
AUTO user id = 2

// 시퀀스 호출 시 값을 1씩 증가시킴
Hibernate:
		call next value for hibernate_sequence

// 기본키에 시퀀스 할당
AUTO user id = 3

// 엔티티를 DB에 저장
Hibernate:
		insert
		into
				user_auto
				(name, id)
		values
				(?, ?)
Hibernate:
		insert
		into
				user_auto
				(name, id)
		values
				(?, ?)
Hibernate:
		insert
		into
				user_auto
				(name, id)
		values
				(?, ?)
```

AUTO 전략의 장점은 DB를 변경해도 코드를 수정할 필요가 없다는 점이다. 그중에서 키 생성 전략이 확정되지 않은 개발 초기단계에서 사용할 경우 매우 편리하다는 점을 들 수 있다.

### 8.7 기본키 매핑 요약

- 직접할당 : entityManager.persist()를 호출하기 전에 애플리케이션에서 직접 식별자 값을 할당해야 한다. 만약 값이 없다면 예외가 발생함
- IDENTITY : DB에 엔티티를 저장해서 식별자 값을 획득한 후 영속성 컨텍스트에 저장함(테이블에 데이터를 저장해야 식별자 값을 획득할 수 있음)
- TABLE : DB 시퀀스 생성 테이블에서 식별자 값을 획득한 후 영속성 컨텍스트에 저장함
- SEQUENCE : DB 시퀀스에서 식별자 값을 획득한 후 영속성 컨텍스트에 저장함

## 9. 필드와 컬럼 매핑 : 레퍼런스(Reference)

---

- 필드와 컬럼 매핑

    1) @Column : 컬럼을 매핑함

    2) @Transient : 특정 필드를 DB에 매핑하지 않음

    3) @Enumerated : Java enum 타입 매핑함

    4) @Lob : BLOB, CLOB 타입을 매핑함

    5) @Temporal : 날짜 타입을 매핑함

- 기타 속성

    1) @Access : JPA가 엔티티에 접근하는 방식을 지정함

### 9.1 @Column

#### 9.1.1 속성

- name 속성 : 필드와 매핑할 테이블 컬럼의 이름 - **기본값은 객체의 필드 이름**
- unique 속성 : 하나의 컬럼에 간단한 유니크 제약조건을 부여할 때 사용하며, 컬럼이 2개 이상일 경우 클래스 레벨에서 사용해야 함
- length 속성 : 문자 길이 제약조건이며 String 타입일 경우에만 사용 - **기본값은 255**
- nullable 속성 : null 값의 허용 여부를 설정 - **기본값은 true**

#### 9.1.2 주의사항

Java의 기본타입의 경우 @Column을 사용하면 nullable = false로 지정하는 것이 안전하다. Java의 기본타입은 null 값을 입력할 수 없기 때문이다.

### 9.2 @Transient

#### 9.2.1 속성

- 객체에 임시로 어떤 값을 보관하고 싶을 경우 사용함
- DB에 저장하지 않으며, 검색 또한 하지 않음

### 9.3 @Enumerate

#### 9.3.1 속성

- EnumType.ORDINAL

    1) 저장된 enum의 순서변경을 할 수 없음

    2) DB에 저장되는 크기가 작음

    3) enum 순서를 DB에 저장함

- EnumType.STRING

    1) 저장된 enum의 순서가 바뀌거나 추가되어도 안전함

    2) DB에 저장되는 크기가 ORDINAL보다 큼

    3) enum 이름을 DB에 저장함

#### 9.3.2 예시

```java
// enum 클래스
enum RoleType {
		ADMIN, USER
}
```

```java
// enum 매핑
@Enumerated(EnumType.STRING)
private RoleType roleType1;

@Enumerated(EnumType.ORDINAL)
private RoleType roleType2;
```

```java
// enum 사용법
user1.setRoleType(roleType1.ADMIN);  // DB에 문자열 타입 ADMIN으로 저장함
user2.setRoleType(roleType2.ADMIN);  // DB에 숫자 타입 0으로 저장함
```

### 9.4 @Lob

#### 9.4.1 속성

- 매핑하는 필드 타입이 문자이면 CLOB으로 매핑, 나머지는 BLOB으로 매핑됨
    - CLOB 속성 : String, char[], java.sql.CLOB
    - BLOB 속성 : byte[], java.sql.BLOB
- 지정할 수 있는 속성이 없음

#### 9.4.2 예시

```java
@Lob
private String lobString;

@Lob
private byte[] lobByte;

// ...
```

### 9.5 @Temporal

#### 9.5.1 속성

- TemporalType.TIME : 시간, DB의 time 타입과 매핑됨 - **예) 06:00:00**
- TemporalType.TIMESTAMP : 날짜, 시간, DB의 timestamp 타입과 매핑됨 - **예) 2020-12-17 13:21:30**

#### 9.5.2 예시

```java
@Temporal(TemporalType.TIME)
private Date time;

@Temporal(TemporalType.TIMESTAMP)
private Date timestamp;

@Temporal(TemporalType.DATE)
private date date;
```

### 9.6 @Access

#### 9.6.1 접근 방식

- 프로퍼티(Property) 접근 : AccessType.PROPERTY로 지정하며, 접근자인 getter를 사용함
- 필드 접근 : AccessType.FIELD로 지정하며, 필드에 직접 접근한다. 접근 권한이 private여도 접근이 가능함

#### 9.6.2 예시

```java
// 프로퍼티 접근 방식
@Entity
@Access(AccessType.PROPERTY)  // 생략 가능함
public class User {
		private String userId;
		// ...
		@Id
		public String getUserId() {
				return userId;
		}
		// ...
}
```

```java
// 필드 접근 방식
@Entity
@Access(AccessType.FIELD)  // 생략 가능함
public class User {
		@Id
		private String userId;
		// ...
}
```

참고로 프로퍼티 접근과 필드 접근 방식을 같이 사용할 수도 있다. 다음의 코드를 통해 확인할 수 있을 것이다.

```java
// 프로퍼티 + 필드 접근 방식
@Entity
public class User {
		@Id
		private String userId;  // 필드 접근 방식 사용함
		@Transient
		private String userName;
		@Transient
		private Integer userAge;
		// ...
		@Access(AccessType.PROPERTY)  // 프로퍼티 접근 방식 사용함
		public String getUserInfo() {
				return userName + userAge;
		}
}
```