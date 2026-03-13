---
layout  : post
title   : jdbcSessionDataSourceInitializer 이슈
summary : '2022-01-06 23:23:12.362 ERROR 14084 - [ main] o.s.boot.SpringApplication : Application run failed'
date    : 2022-01-06 23:25:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : notion import
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# jdbcSessionDataSourceInitializer 이슈
Created: 2022년 1월 6일 오후 11:25
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

# 주제 :

```jsx
2022-01-06 23:23:12.362 ERROR 14084 --- [           main] o.s.boot.SpringApplication               : Application run failed

java.lang.IllegalStateException: Error processing condition on org.springframework.boot.autoconfigure.session.JdbcSessionConfiguration.jdbcSessionDataSourceInitializer
	at org.springframework.boot.autoconfigure.condition.SpringBootCondition.matches(SpringBootCondition.java:60) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.context.annotation.ConditionEvaluator.shouldSkip(ConditionEvaluator.java:108) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.annotation.ConfigurationClassBeanDefinitionReader.loadBeanDefinitionsForBeanMethod(ConfigurationClassBeanDefinitionReader.java:181) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.annotation.ConfigurationClassBeanDefinitionReader.loadBeanDefinitionsForConfigurationClass(ConfigurationClassBeanDefinitionReader.java:141) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.annotation.ConfigurationClassBeanDefinitionReader.loadBeanDefinitions(ConfigurationClassBeanDefinitionReader.java:117) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.annotation.ConfigurationClassPostProcessor.processConfigBeanDefinitions(ConfigurationClassPostProcessor.java:327) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.annotation.ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry(ConfigurationClassPostProcessor.java:232) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.support.PostProcessorRegistrationDelegate.invokeBeanDefinitionRegistryPostProcessors(PostProcessorRegistrationDelegate.java:275) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.support.PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors(PostProcessorRegistrationDelegate.java:95) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.invokeBeanFactoryPostProcessors(AbstractApplicationContext.java:705) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:531) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:141) ~[spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:744) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:391) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:312) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1215) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1204) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at kr.co.shelter.Application.main(Application.java:11) [classes/:na]
Caused by: java.lang.IllegalStateException: Failed to introspect Class [org.springframework.session.jdbc.config.annotation.web.http.JdbcHttpSessionConfiguration] from ClassLoader [sun.misc.Launcher$AppClassLoader@18b4aac2]
	at org.springframework.util.ReflectionUtils.getDeclaredMethods(ReflectionUtils.java:507) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:404) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:417) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:389) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.util.ReflectionUtils.getUniqueDeclaredMethods(ReflectionUtils.java:447) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at java.util.concurrent.ConcurrentHashMap.computeIfAbsent(ConcurrentHashMap.java:1688) ~[na:1.8.0_275]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.getTypeForFactoryMethod(AbstractAutowireCapableBeanFactory.java:738) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.determineTargetType(AbstractAutowireCapableBeanFactory.java:679) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.predictBeanType(AbstractAutowireCapableBeanFactory.java:647) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.isFactoryBean(AbstractBeanFactory.java:1518) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.isFactoryBean(AbstractBeanFactory.java:1023) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.boot.autoconfigure.condition.BeanTypeRegistry.addBeanTypeForNonAliasDefinition(BeanTypeRegistry.java:189) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.BeanTypeRegistry.addBeanTypeForNonAliasDefinition(BeanTypeRegistry.java:156) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.BeanTypeRegistry.addBeanType(BeanTypeRegistry.java:149) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.BeanTypeRegistry.updateTypesIfNecessary(BeanTypeRegistry.java:137) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at java.util.Iterator.forEachRemaining(Iterator.java:116) ~[na:1.8.0_275]
	at org.springframework.boot.autoconfigure.condition.BeanTypeRegistry.updateTypesIfNecessary(BeanTypeRegistry.java:132) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.BeanTypeRegistry.getNamesForType(BeanTypeRegistry.java:96) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.OnBeanCondition.collectBeanNamesForType(OnBeanCondition.java:269) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.OnBeanCondition.getBeanNamesForType(OnBeanCondition.java:262) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.OnBeanCondition.getBeanNamesForType(OnBeanCondition.java:251) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.OnBeanCondition.getMatchingBeans(OnBeanCondition.java:171) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.OnBeanCondition.getMatchOutcome(OnBeanCondition.java:145) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.autoconfigure.condition.SpringBootCondition.matches(SpringBootCondition.java:47) ~[spring-boot-autoconfigure-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	... 17 common frames omitted
Caused by: java.lang.NoClassDefFoundError: org/springframework/session/FlushMode
	at java.lang.Class.getDeclaredMethods0(Native Method) ~[na:1.8.0_275]
	at java.lang.Class.privateGetDeclaredMethods(Class.java:2701) ~[na:1.8.0_275]
	at java.lang.Class.getDeclaredMethods(Class.java:1975) ~[na:1.8.0_275]
	at org.springframework.util.ReflectionUtils.getDeclaredMethods(ReflectionUtils.java:489) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	... 40 common frames omitted
Caused by: java.lang.ClassNotFoundException: org.springframework.session.FlushMode
	at java.net.URLClassLoader.findClass(URLClassLoader.java:382) ~[na:1.8.0_275]
	at java.lang.ClassLoader.loadClass(ClassLoader.java:419) ~[na:1.8.0_275]
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:352) ~[na:1.8.0_275]
	at java.lang.ClassLoader.loadClass(ClassLoader.java:352) ~[na:1.8.0_275]
	... 44 common frames omitted

2022-01-06 23:23:12.366  WARN 14084 --- [           main] o.s.boot.SpringApplication               : Unable to close ApplicationContext

java.lang.IllegalStateException: Failed to introspect Class [org.springframework.session.jdbc.config.annotation.web.http.JdbcHttpSessionConfiguration] from ClassLoader [sun.misc.Launcher$AppClassLoader@18b4aac2]
	at org.springframework.util.ReflectionUtils.getDeclaredMethods(ReflectionUtils.java:507) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:404) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:417) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:389) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.util.ReflectionUtils.getUniqueDeclaredMethods(ReflectionUtils.java:447) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at java.util.concurrent.ConcurrentHashMap.computeIfAbsent(ConcurrentHashMap.java:1688) ~[na:1.8.0_275]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.getTypeForFactoryMethod(AbstractAutowireCapableBeanFactory.java:738) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.determineTargetType(AbstractAutowireCapableBeanFactory.java:679) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.predictBeanType(AbstractAutowireCapableBeanFactory.java:647) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.isFactoryBean(AbstractBeanFactory.java:1518) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doGetBeanNamesForType(DefaultListableBeanFactory.java:513) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBeanNamesForType(DefaultListableBeanFactory.java:483) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBeansOfType(DefaultListableBeanFactory.java:604) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBeansOfType(DefaultListableBeanFactory.java:596) ~[spring-beans-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.getBeansOfType(AbstractApplicationContext.java:1226) ~[spring-context-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	at org.springframework.boot.SpringApplication.getExitCodeFromMappedException(SpringApplication.java:866) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.getExitCodeFromException(SpringApplication.java:854) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.handleExitCode(SpringApplication.java:841) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.handleRunFailure(SpringApplication.java:792) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:322) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1215) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1204) [spring-boot-2.1.9.RELEASE.jar:2.1.9.RELEASE]
	at kr.co.shelter.Application.main(Application.java:11) [classes/:na]
Caused by: java.lang.NoClassDefFoundError: org/springframework/session/FlushMode
	at java.lang.Class.getDeclaredMethods0(Native Method) ~[na:1.8.0_275]
	at java.lang.Class.privateGetDeclaredMethods(Class.java:2701) ~[na:1.8.0_275]
	at java.lang.Class.getDeclaredMethods(Class.java:1975) ~[na:1.8.0_275]
	at org.springframework.util.ReflectionUtils.getDeclaredMethods(ReflectionUtils.java:489) ~[spring-core-5.1.10.RELEASE.jar:5.1.10.RELEASE]
	... 22 common frames omitted
Caused by: java.lang.ClassNotFoundException: org.springframework.session.FlushMode
	at java.net.URLClassLoader.findClass(URLClassLoader.java:382) ~[na:1.8.0_275]
	at java.lang.ClassLoader.loadClass(ClassLoader.java:419) ~[na:1.8.0_275]
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:352) ~[na:1.8.0_275]
	at java.lang.ClassLoader.loadClass(ClassLoader.java:352) ~[na:1.8.0_275]
	... 26 common frames omitted

Process finished with exit code 1
```

- dependency  버전 호환 이슈일 수 있다고 함
    
    → implementation 디비 관련된 거 다 날려버림
    

```jsx
dependencies {
    implementation('org.springframework.boot:spring-boot-starter-data-jpa')
    implementation('org.springframework.boot:spring-boot-starter-thymeleaf')
    implementation('org.springframework.boot:spring-boot-starter-web')
    implementation('org.projectlombok:lombok:1.18.22')
    implementation('org.springframework.boot:spring-boot-starter-mustache:2.6.1')

//    implementation('org.springframework.boot:spring-boot-starter-oauth2-client:2.6.1')

}→ 
```

```jsx
***************************
APPLICATION FAILED TO START
***************************

Description:

Failed to bind properties under '' to com.zaxxer.hikari.HikariDataSource:

    Property: driverclassname
    Value: com.mysql.cj.jdbc.Driver
    Origin: "driverClassName" from property source "source"
    Reason: Failed to load driver class com.mysql.cj.jdbc.Driver in either of HikariConfig class loader or Thread context classloader

Action:

Update your application's configuration

Process finished with exit code 1
```

> 리뷰 :
>
