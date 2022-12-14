## FlaskBlog

![img_11.png](Development-Documentation/img_21.png)

## 简介

本博客代码是跟随[bilibili-up-轻编程](https://space.bilibili.com/432627585) 原创开发的flaskblog学习成果，后续会在此基础上完善部分功能。

请尊重原创，思路和大部分代码属于“轻编程”的视频教程，想要跟随学习可以关注他 [bilibili-up-轻编程](https://space.bilibili.com/432627585)

涉及到的功能模块如下：

* 登录
* 注册
* 后台管理
* 分类管理
* 文章管理
* 用户管理
* 全站导航菜单栏
* 文章列表
* 文章详情
* 集成富文本编辑器
* 侧边栏文章归档
* 权限管理
* banner轮播图管理


## 快速体验
<details>
<summary>👉快速体验</summary>
采用docker-compose+shell的方式只需两步就可以部署完成，利于大家快速体验。

**前提条件：** 

①机器可以连接外网； 

②安装docker和docker-compose； 

没安装可以参照[install_docker.sh](https://github.com/LiuShiYa-github/ShellScript/blob/main/install_docker.sh)

**部署FlaskBlog**
```text
① git clone  https://github.com/LiuShiYa-github/FlaskBlog.git
② bash  FlaskBlog/docker-deploy/deploy.sh
访问http://ipaddress
账户名密码：admin/admin
```
![img_11.png](Development-Documentation/img_19.png)
</details>


## 效果展示
<details>
<summary>👉效果展示</summary>

首页

![img_11.png](Development-Documentation/img_11.png)



管理后台

![img_1.png](Development-Documentation/img_8.png)

文章管理

![img_9.png](Development-Documentation/img_9.png)


用户管理

![img_10.png](Development-Documentation/img_10.png)

banner轮播图管理

![img_12.png](Development-Documentation/img_12.png)


登录

![img_13.png](Development-Documentation/img_13.png)

注册

![img_14.png](Development-Documentation/img_14.png)

侧边栏搜索
![img_15.png](Development-Documentation/img_15.png)

![img_16.png](Development-Documentation/img_16.png)

文章详情
![img_17.png](Development-Documentation/img_17.png)
</details>


## 开发文档
<details>
<summary>👉开发文档</summary>

开发过程&遇到的问题&现存bug都在[开发文档](https://github.com/LiuShiYa-github/FlaskBlog/tree/master/Development-Documentation) 中记录

</details>

