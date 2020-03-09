from base import *


driver = webdriver.Chrome(DRIVER_DIR)

existing_list = glob.glob(f'{EXISTING_LIST_DIR}*.txt')
for path in existing_list:
    # txt 파일 이름에 가끔 \\ 이 있는 현상 발생하므로 replace 처리
    if '\\' in path:
        path = path.replace('\\', '/')

    user_id = path.split(EXISTING_LIST_DIR)[1]
    user_id = user_id.split('.txt')[0]

    # 기존 크롤링했던 상세링크 url들 setting
    f = open(path, 'r')
    lines = f.readlines()
    existring_page_urls = []
    for line in lines:
        value = line.replace('\n', '')
        existring_page_urls.append(value)
    f.close()

    driver_url = f'https://www.instagram.com/{user_id}/'
    driver.get(driver_url)
    time.sleep(2)

    # 해당 계정으로 가서 최근 10개의 상세 링크들 list 화
    detail_page_urls = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    a_tag_list = soup.find_all('a')
    for a_tag in a_tag_list:
        if '/p/' in a_tag['href']:
            detail_page_urls.append(a_tag['href'])
    if len(detail_page_urls) > 10:
        detail_page_urls = detail_page_urls[:10]

    # 상세링크가 없다면 다음 계정으로 continue
    if not detail_page_urls:
        continue

    # 해당 txt파일 추가가능 형태로 open
    f = open(path, 'a')

    for url in detail_page_urls:

        # 이미 크롤링했던 상세링크라면 다음으로 continue 처리
        if url in existring_page_urls:
            continue

        # 새롭게 txt파일에 링크 추가
        f.write(f'{url}\n')

        driver.get(f'https://www.instagram.com{url}')
        check_right_arrow = True

        image_src_list = []
        video_src_list = []

        # 링크 상세로 들어가 오른쪽으로 이동하는 화살표 태그가 있는지 체크
        # 있으면 계속 image url을 list에 담는다
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

            # 더이상 오른쪽을 클릭할수 없으면 while 문을 빠져나온다
            try:
                right_arrow = 'div.coreSpriteRightChevron'
                element_to_click = driver.find_element_by_css_selector(
                    right_arrow
                )
                actions = ActionChains(driver)
                actions.move_to_element(element_to_click).click().perform()
                time.sleep(0.3)
            except:
                check_right_arrow = False

        # image file save
        for image_src in image_src_list:
            file_name = create_file_name()
            file_name = f'{user_id}_{file_name}'
            urllib.request.urlretrieve(
                image_src,
                f'{IMAGES_DIR}{file_name}.png'
            )

        # mp4 file save
        for video_src in video_src_list:
            file_name = create_file_name()
            file_name = f'{user_id}_{file_name}'
            video_name = f'{MOVIES_DIR}{file_name}.mp4'
            urllib.request.urlretrieve(video_src, video_name)

            # saved mp4 file to gif
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

    f.close()

driver.close()
