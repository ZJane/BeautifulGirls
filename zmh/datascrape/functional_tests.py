from selenium import webdriver

brower = webdriver.PhantomJS()
brower.get("http://localhost:8080")
assert 'Django' in brower.title
