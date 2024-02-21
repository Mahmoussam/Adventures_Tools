from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService

# Path to the Microsoft Edge WebDriver executable
edge_driver_path = "edgedriver_w64/msedgedriver.exe"  
edge_options = webdriver.EdgeOptions()
edge_options.use_chromium = True  # This is required for recent versions of Microsoft Edge
uag="Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10.0 b8asd98ads8a7fhhgj/2.0.0.1)"
edge_options.add_argument("user-agent="+"apachiano")
edge_options.add_argument("GUID="+"4440-1321-1321-9797")

# Create a new instance of the Edge driver with the specified options
driver = webdriver.Edge(service=EdgeService(edge_driver_path), options=edge_options)

driver.get("https://site-to-test.com")
