# API Testing Practice

API testing validates service behavior, contract stability, integration correctness, security, and reliability across microservices and enterprise platforms.

## Core Topics

- REST API testing
- SOAP service validation
- Postman collections
- ReadyAPI / SOAPUI
- REST Assured automation
- Contract testing
- Schema validation
- OAuth and authentication
- Negative testing
- Error handling
- Idempotency and retries

## REST Assured Sketch

```java
given()
    .baseUri(baseUrl)
    .header("Authorization", "Bearer " + token)
.when()
    .get("/payments/{id}", paymentId)
.then()
    .statusCode(200)
    .body("status", notNullValue());
```

## Generated Examples

- [API Testing Example 1](../solutions/generated/API-00006/)
- [API Testing Example 2](../solutions/generated/API-00078/)
- [API Testing Example 3](../solutions/generated/API-00150/)
