from msilib.schema import tables
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Category, Post, Tag, Comment

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_hyo = User.objects.create_user(username='hyo', password='pass1234')
        self.category_movie = Category.objects.create(name='movie', slug='movie')

        self.user_obama = User.objects.create_user(username='obama', password='somepassword')
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')

        self.user_obama.is_staff = True
        self.user_obama.save()

        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        self.post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
            author = self.user_hyo
        )
        self.post_001.tags.add(self.tag_hello)
        
        self.post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = '여러분 잘 따라오고 계시죠?',
            category = self.category_movie, 
            author = self.user_hyo
        )
        
        self.post_003 = Post.objects.create(
            title = '세 번째 포스트입니다.',
            content = '졸려',
            category = self.category_movie, 
            author = self.user_hyo
        )
        self.post_003.tags.add(self.tag_python)
        self.post_003.tags.add(self.tag_python_kor)

        self.comment_001 = Comment.objects.create(
            post = self.post_001,
            author = self.user_obama,
            content = '첫 번째 댓글입니다.'
        )
        

    def category_card_test(self, soup) :
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(
            f'{self.category_movie.name} ({self.category_movie.post_set.count()})',
            categories_card.text
        )
        self.assertIn(f'미분류 (1)', categories_card.text)

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
        
        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')
        
        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')
        
        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')
        
        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')
    
    def test_post_list(self):
        
        #포스트 개수 체크
        self.assertEqual(Post.objects.count(), 3)

        #1. 포스트 목록 페이지
        response = self.client.get('/blog/')
        #2. 정상적으로 페이지가 로드되는 것
        self.assertEqual(response.status_code, 200)
        #3. 페이지 타이틀 'Blog'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        #4. 내비게이션 바 존재한다.
        #5. Blog, About Me 라는 문구가 내비게이션 바에 있다.
        self.navbar_test(soup)

        #카테고리 테스트
        self.category_card_test(soup)
        
        '''
        #1. 메인 영역에 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        #2. '아직 게시물이 없습니다.' 라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        '''

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        '''
        #1. 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
            author = self.user_hyo
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content = '여러분 잘 따라오고 계시죠?',
            author = self.user_hyo
        )
        self.assertEqual(Post.objects.count(), 2)
        
        #2. 포스트 목록 페이지를 새로고침 했을때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        #3. 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        #4. '아직 게시물이 없습니다.'라는 문구가 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
        #5. 유저명이 나타난다.
        self.assertIn(self.user_hyo.username.upper(), main_area.text)
        '''
        post_001_card = main_area.find('div', id='post-1')
        self.assertIn('미분류', post_001_card.text)
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.user_hyo.username.upper(), main_area.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)
           
        post_003_card = main_area.find('div', id='post-3')
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)
        #포스트가 없다면
        Post.objects.all().delete()
        #1. 메인 영역에 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        #새로 정보 가져오기
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        #2. '아직 게시물이 없습니다.' 라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text) 


    def test_post_detail(self):
        '''
        #1.포스트가 하나 있다
        post_001 = Post.objects.create (
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world',
            author = self.user_hyo
        )
        '''

        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')
        
        '''
        #1. 첫 번째 포스트의 상세 페이지 테스트
        #2. 첫 번째 포스트의 url 로 접근하면 정상적으로 작동한다. (status code : 200)
        '''
        response= self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #3. 포스트 목록 페이지와 똑같은 네비게이션 바가 있다.
        self.navbar_test(soup)
        self.category_card_test(soup)

        '''
        #4. 첫 번째 포스트의 제목이 웹 브라우저 타이틀에 들어있다.
        '''
        self.assertIn(self.post_001.title, soup.title.text)
        
        '''
        #5. 첫 번째 포스트의 제목이 포스트 영역에 있다.
        '''
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        # self.assertIn(self.category_movie.name, post_area.text)

        #6. 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다 (아직 구현할 수 없음)
        #아직 작성 불가
        
        #7. 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)

        #8. 유저명이 나타난다.
        self.assertIn(self.user_hyo.username.upper(), post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)

        comments_area = soup.find('div', id='comment-area')
        comment_001_area = comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)
                

    def test_category_page(self) : 
        response = self.client.get(self.category_movie.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_movie.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_movie.name, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_001.title, main_area.text)

    def test_tag_page(self) :
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)

    def test_create_post(self) :
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)
        
        self.client.login(username='trump', password="somepassword")
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='obama', password="somepassword")
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post/',
            {
                'title' : 'Post Form 만들기',
                'content' : 'Post Form 페이지를 만듭시다',
                'tags_str' : 'new tag; 한글 태그, python'
            }
        )
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, 'Post Form 만들기')
        self.assertEqual(last_post.author.username, 'obama')

        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        self.assertEqual(Tag.objects.count(), 5)

    def test_update_post(self) :
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username = self.user_trump.username,
            password = 'somepassword'
        )

        response= self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        self.client.login(
            username = self.post_003.author.username,
            password = "pass1234"
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)
        
        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('파이썬 공부;python', tag_str_input.attrs['value'])

        response = self.client.post (
            update_post_url,
            {
                'title' : '세 번째 포스트를 수정했습니다.',
                'content' : '안녕 세계? 우리는 하나!',
                'category' : self.category_movie.pk,
                'tags_str' : '파이썬 공부; 한글 태그, some tag'
            },
            follow=True
        )

        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)
        self.assertIn(self.category_movie.name, main_area.text)
        self.assertIn('파이썬 공부', main_area.text)
        self.assertIn('한글 태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python', main_area.text)

    def test_comment_form(self) :
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertIn('Log in and leave a comment', comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))

        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Log in and leave a comment', comment_area.text)

        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content' : '오바마의 댓글입니다.'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)        

        new_comment = Comment.objects.last()

        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)

        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('obama', new_comment_div.text)
        self.assertIn('오바마의 댓글입니다.', new_comment_div.text)

def test_comment_update(self) :
    comment_by_trump = Comment.objects.create (
        post = self.post_001,
        author = self.user_trump,
        content = '트럼프의 댓글입니다.'
    )

    response = self.client.get(self.post_001.get_absolute_url())
    self.assertEqual(response.status_code, 200)
    soup = BeautifulSoup(response.content, 'html.parser')

    comment_area = soup.find('div', id='comment-area')
    self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
    self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

    self.client.login(username='obama', password='somepassword')
    response = self.client.get(self.post_001.get_absolute_url())
    self.assertEqual(response.status_code, 200)
    soup = BeautifulSoup(response.content, 'html.parser')

    comment_area = soup.find('div', id='comment-area')
    self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
    comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn')
    self.assertIn('edit', comment_001_update_btn.text)
    self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')
    
    response = self.client.get('/blog/update_comment/1/')
    self.assertEqual(response.status_code, 200)

    soup = BeautifulSoup(response.content, 'html.parser')

    self.assertEqual('Edit Comment - Blog', soup.title.text)
    update_comment_form = soup.find('form', id='comment-form')
    content_textarea = update_comment_form.find('textarea', id='id-content')
    self.assertIn(self.comment_001.content, content_textarea.text)

    response = self.client.post(
        f'/blog/update_comment/{self.comment_001.pk}/',
        {
            'content' : '오바마의 댓글을 수정합니다.',
        },
        follow=True
    )

    self.assertEqual(response.status_code, 200)
    soup = BeautifulSoup(response.content, 'html.parser')
    comment_001_div = soup.find('div', id='comment-1')
    self.assertIn('오바마의 댓글을 수정합니다.', comment_001_div.text)
    self.assertIn('Updated: ', comment_001_div.text)