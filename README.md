# chromedriver-bug
This repository demonstrates issue between ChromeDriver and Selenium for latest versions of Chromium/Chrome
Last known working version is Chromium 128 with it's  ChromeDriver

Old Chromium: 128
Old ChromeDriver: 128.0.6613.119

Latest test version Chrome: 140.0.7339.185

The problem is reproducible with the provided unittest script: [test_browser_correctly_navigates.py](test_browser_correctly_navigates.py)

Related issue: https://issues.chromium.org/issues/402796660



## Environment Setup
```
python3.12 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Driver Setup
1. Download chromium 128 package http://packages.linuxmint.com/pool/upstream/c/chromium/chromium_128.0.6613.119~linuxmint1%2Belsie_amd64.deb
2. Install chromium with driver `sudo dpkg -i chromium_128.0.6613.119~linuxmint1+elsie_amd64.deb`

Make sure it's executable:
`chmod +x chromedriver`

## Running the Script
activate the virtual env.
1. for Chromium 128 use `USE_CHROMIUM128=1 python3 -m unittest -v test_browser_correctly_navigates.py`
2. for new chrome just use `python3 -m unittest -v test_browser_correctly_navigates.py`


## Actual results
Test with Chromium 128 is passing. See output file [test_output_chromium128_passed.txt](test_output_chromium128_passed.txt)
Test with Crhome 140.0.7339.185 is failing. See output file [test_output_latest_chrome_fail.txt](test_output_latest_chrome_fail.txt)
