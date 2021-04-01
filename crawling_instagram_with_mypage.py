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
time.sleep(5)

# txt 파일에 detail page url 전부 저장
body = driver.find_element_by_tag_name('body')
last_height = driver.execute_script('return document.body.scrollHeight')

image_src_list = []

while True:
    body.send_keys(Keys.END)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    image_tag_list = soup.select('img.FFVAD')
    for image_tag in image_tag_list:
        try:
            image_tag_src = image_tag['src']
            image_src_list.append(image_tag_src)
        except Exception as e:
            print(str(e))
            continue

    # 마지막 스크롤인지 체크
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height


# image file save
for image_src in image_src_list:
    try:
        file_name = create_file_name()
        urllib.request.urlretrieve(
            image_src,
            f'{IMAGES_DIR}{file_name}.png'
        )
    except Exception as e:
        print(str(e))
        continue


# exit
time.sleep(1)
driver.close()
