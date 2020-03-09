from base import *


# 태그 키워드 지정
keyword = input('tag keyword: ')
if not keyword:
    print('keyword is none')
    sys.exit()

# 스크롤 다운 횟수 지정
num_of_pagedowns = int(input('num_of_pagedowns: '))
if not num_of_pagedowns:
    num_of_pagedowns = 1

# driver setting
driver = webdriver.Chrome(DRIVER_DIR)
driver_url = f'https://www.instagram.com/explore/tags/{keyword}/'
driver.get(driver_url)
time.sleep(2)

# page down 하면서 상세링크주소값들 list화
detail_page_urls = []
body = driver.find_element_by_tag_name('body')
while num_of_pagedowns:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    a_tag_list = soup.find_all('a')

    for a_tag in a_tag_list:
        if '/p/' in a_tag['href']:
            detail_page_urls.append(a_tag['href'])

    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)
    num_of_pagedowns -= 1

# 상세링크 리스트에서 중복 값들 제거
detail_page_urls = list(set(detail_page_urls))
print(f'total count: {len(detail_page_urls)}')

for i, url in enumerate(detail_page_urls):
    driver.get(f'https://www.instagram.com{url}')
    check_right_arrow = True

    image_src_list = []
    video_src_list = []

    # 상세링크의 계정 id 값 get 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    a_tag_list = soup.findAll('a', {'class': 'FPmhX notranslate nJAzx'})
    try:
        user_id = a_tag_list[0]['title']
    except:
        user_id = 'none'

    # 상세링크의 오른쪽 버튼 이동 스크립트
    while check_right_arrow:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        image_tag_list = soup.find_all('img')
        for image_tag in image_tag_list:
            image_tag_src = image_tag['src']
            image_tag_alt = image_tag['alt']
            if not '프로필' in image_tag_alt:
                if not image_tag_src in image_src_list:
                    image_src_list.append(image_tag_src)

        video_tag_list = soup.find_all('video')
        for video_tag in video_tag_list:
            video_tag_src = video_tag['src']
            if not video_tag_src in video_src_list:
                video_src_list.append(video_tag_src)

        # 오른쪽 클릭 불가일 경우 while 탈출
        try:
            right_arrow = 'div.coreSpriteRightChevron'
            element_to_click = driver.find_element_by_css_selector(right_arrow)
            actions = ActionChains(driver)
            actions.move_to_element(element_to_click).click().perform()
            time.sleep(0.3)
        except:
            check_right_arrow = False

    # image file save
    for image_src in image_src_list:
        file_name = create_file_name()
        file_name = f'{user_id}_{file_name}'
        urllib.request.urlretrieve(image_src, f'{IMAGES_DIR}{file_name}.png')

    # mp4 file save
    for video_src in video_src_list:
        file_name = create_file_name()
        file_name = f'{user_id}_{file_name}'
        video_name = f'{MOVIES_DIR}{file_name}.mp4'
        urllib.request.urlretrieve(video_src, video_name)

        # mp4 file to gif
        try:
            clip = VideoFileClip(video_name)
            end_t = round(clip.duration) - 1
            start_t = 1 if end_t > 1 else 0
            end_t = 3 if end_t > 3 else end_t

            snapshot = clip.subclip(start_t, end_t).resize(0.3)
            gif_name = f'{IMAGES_DIR}{file_name}.gif'
            snapshot.write_gif(gif_name)

            clip.close()

        except Exception as e:
            print(str(e))
            continue

    print(i)

driver.close()
