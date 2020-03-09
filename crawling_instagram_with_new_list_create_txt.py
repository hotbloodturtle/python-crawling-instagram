from base import *


# chrome driver 세팅
driver = webdriver.Chrome(DRIVER_DIR)

f = open('./new_list.txt', 'r')
user_id_list = f.readlines()
for user_id in user_id_list:
    if '\\' in user_id:
        user_id = user_id.replace('\\', '')
    if '\n' in user_id:
        user_id = user_id.replace('\n', '')
    
    driver_url = f'https://www.instagram.com/{user_id}/'
    driver.get(driver_url)
    time.sleep(2)
    
    # txt 파일에 detail page url 전부 저장
    body = driver.find_element_by_tag_name('body')
    last_height = driver.execute_script('return document.body.scrollHeight')
    urls = []
    
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    
        # 상세페이지 a 태그만 list append
        a_tag_list = soup.find_all('a')
        for a_tag in a_tag_list:
            if '/p/' in a_tag['href']:
                urls.append(a_tag['href'])
    
        body.send_keys(Keys.END)
        time.sleep(2)
    
        # 마지막 스크롤인지 체크
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
		
    # list 중복 제거 및 txt 파일로 저장
    f = open(f'{NEW_LIST_DIR}{user_id}.txt', 'w')
    urls = list(set(urls))
    for url in urls:
        f.write(f'{url}\n')
    f.close()

# 완료 후 txt 내용 초기화
f = open('./new_list.txt', 'w')
f.close()

driver.close()

