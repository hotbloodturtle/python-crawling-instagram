from base import *


# driver setting
driver = webdriver.Chrome(DRIVER_DIR)

# txt list
txt_list = glob.glob(f'{NEW_LIST_DIR}*.txt')
for path in txt_list:
    # txt 파일 이름에 가끔 \\ 이 있는 현상 발생하므로 replace 처리
    if '\\' in path:
        path = path.replace('\\', '/')

    # txt 파일안에 상세 링크 주소들 list 형태로 get
    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    user_id = path.split(NEW_LIST_DIR)[1]
    user_id = user_id.split('.txt')[0]

    # 상세 url 크롤링 횟수, 한번도 하지 않으면 이미 다 크롤링했으니 txt제거
    crawling_count = 0

    for line in lines:

        # 이미 한번 크롤링한 계정은 상세링크들이 content 안에 있고
        # 이미 크롤링한 상세 링크는 continue 처리
        line = line.replace('\n', '')
        try:
            f = open(f'./existing_list/{user_id}.txt', 'r')
            content = f.read()
            f.close()

            if line in content:
                continue
        # 에러 발생시 처음으로 크롤링 하는 계정이므로 pass 처리
        except:
            pass

        crawling_count += 1

        url = f'https://www.instagram.com{line}'

        driver.get(url)
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
        
        # 크롤링 완료시 txt에 url 저장
        f = open(f'./existing_list/{user_id}.txt', 'a')
        f.write(f'{line}\n')
        f.close()

    # 크롤링 카운트 체크, 0 이라면 txt 내용 초기화
    f = open(path, 'w')
    f.close()

driver.close()
        


