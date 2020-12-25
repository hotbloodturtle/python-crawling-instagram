from base import *

USERNAME = input('username: ')
PASSWORD = input('password: ')

# driver setting
driver = webdriver.Chrome(DRIVER_DIR)
driver.get('https://www.instagram.com/accounts/login/')

time.sleep(1)


element_id = driver.find_element_by_name('username')
element_password = driver.find_element_by_name('password')
element_id.send_keys(USERNAME)
element_password.send_keys(PASSWORD)
element_password.submit()

time.sleep(5)
driver.get(f'https://www.instagram.com/{USERNAME}/saved/')

# txt 파일에 detail page url 전부 저장
body = driver.find_element_by_tag_name('body')
last_height = driver.execute_script('return document.body.scrollHeight')
urls = []


f = open(f'{MYPAGE_LIST_DIR}mylist.txt', 'r')
lines = f.readlines()
existring_src_list = []
for line in lines:
    value = line.replace('\n', '')
    existring_src_list.append(value)
f.close()

image_src_list = []
s_count = 0

while True:
    body.send_keys(Keys.END)
    time.sleep(2)

    # if s_count == 3:
    #     break

    # 마지막 스크롤인지 체크
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    image_tag_list = soup.select('img.FFVAD')
    for image_tag in image_tag_list:
        try:
            image_tag_src = image_tag['src']
            if image_tag_src in existring_src_list or image_tag_src in image_src_list:
                continue
            image_src_list.append(image_tag_src)
        except Exception as e:
            print(str(e))
            continue

    s_count += 1


f = open(f'{MYPAGE_LIST_DIR}mylist.txt', 'a')


# image file save
for image_src in image_src_list:
    try:
        file_name = create_file_name()
        urllib.request.urlretrieve(
            image_src,
            f'{IMAGES_DIR}{file_name}.png'
        )
        f.write(f'{image_src}\n')
    except Exception as e:
        print(str(e))
        continue


# exit
time.sleep(1)
f.close()
driver.close()
