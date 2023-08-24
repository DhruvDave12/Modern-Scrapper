import json
import os
from PIL import Image
from selenium import webdriver 
from selenium.webdriver.common.by import By

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")
driver = webdriver.Chrome(options=chromeOptions)
driver.maximize_window();


# whole developers thing of superfluid
SUPERFLUID_DEV_URLS = [
                 "https://docs.superfluid.finance/superfluid/protocol-overview/what-is-superfluid",
                 "https://docs.superfluid.finance/superfluid/developers/quickstart",
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/super-tokens-solidity",
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/super-token-operations",
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/using-super-tokens",
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/types-of-super-tokens",
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/deploy-a-super-token/deployment",
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/deploy-a-super-token/deploying-a-pure-super-token",
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/super-tokens/tracking-super-token-balances",
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/super-tokens/erc777-in-super-tokens"
                 "https://docs.superfluid.finance/superfluid/developers/super-tokens/super-token-faucet",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/read-methods",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/read-methods/getflowinfo",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/read-methods/getflowrate",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/read-methods/getnetflowrate",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/createflow",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/updateflow",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/deleteflow",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/setflowpermissions",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/setmaxflowpermissions",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/revokeflowpermissions",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/createflowfrom",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/updateflowfrom",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/deleteflowfrom",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/with-user-data",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfav1-library/write-methods/with-context",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/read-methods",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/read-methods/getflow",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/read-methods/getnetflow",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/read-methods/getaccountflowinfo",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods/createflow",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods/updateflow",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods/deleteflow",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods/createflowbyoperator",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods/updateflowbyoperator",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods/deleteflowbyoperator",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods/updateflowoperatorpermissions",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-operations/write-methods/revokeflowoperatorpermissions",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/money-streaming-1",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-access-control-list-acl",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/cfa-access-control-list-acl/acl-features",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/more...",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/more.../flow-rate-time-frames",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/more.../building-batched-streams-in-safe",
                 "https://docs.superfluid.finance/superfluid/developers/constant-flow-agreement-cfa/more.../flow-nfts",
                 "https://docs.superfluid.finance/superfluid/developers/instant-distribution-agreement-ida",
                 "https://docs.superfluid.finance/superfluid/developers/instant-distribution-agreement-ida/idav1-library",
                 "https://docs.superfluid.finance/superfluid/developers/instant-distribution-agreement-ida/ida-operations",
                 "https://docs.superfluid.finance/superfluid/developers/instant-distribution-agreement-ida/instant-distribution",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps/super-app",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps/super-app-callbacks",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps/super-app-callbacks/calling-agreements-in-super-apps",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps/user-data",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps/user-data/nft-billboard-example",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps/superappbaseflow",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps/super-app-examples",
                 "https://docs.superfluid.finance/superfluid/developers/super-apps/super-app-deployment-guide",
                 "https://docs.superfluid.finance/superfluid/developers/batch-calls",
                 "https://docs.superfluid.finance/superfluid/developers/batch-calls/batch-calls",
                 "https://docs.superfluid.finance/superfluid/developers/batch-calls/batching-transactions",
                 "https://docs.superfluid.finance/superfluid/developers/automations",
                 "https://docs.superfluid.finance/superfluid/developers/automations/auto-wrap",
                #  https://www.notion.so/oauth2callback?state=eyJjYWxsYmFja1R5cGUiOiJwb3B1cCIsImVuY3J5cHRlZFRva2VuIjoidjAyOmxvZ2luX3dpdGhfZ29vZ2xlOkZhbS1memZNQmdTbjVaZDZtUERJZTR0OEJxaVZCbUJ5ZzQyTDRYT1JUUTN4c2NIRDZXNC1vbVU4MDNhWlhGNnU3YVBGbTZCOHdIUXRtazFFVXNCZzh0Q2JLdW1DQm9WTHVvZkgzQTNiWnNzekdjNTBrVllGQlNlcWhfVFZHUnN2N0JiTSJ9&code=4%2F0Adeu5BWH90oMY4cfWT3cDTaeP4rWzENRqkein3U5olBZwwTMbVQrBcUcr1eLSNNDtO96EQ&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+openid&authuser=0&prompt=consent
                "https://docs.superfluid.finance/superfluid/developers/automations/stream-scheduler",
                # ISKI BHI DAALO NOTION LINK SS
                "https://docs.superfluid.finance/superfluid/developers/automations/vesting-scheduler",
                "https://docs.superfluid.finance/superfluid/developers/automations/stream-accounting-api",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/for-your-integration-the-basics",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/for-your-integration-the-basics/supporting-super-tokens",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/for-your-integration-the-basics/supporting-money-streams",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/for-your-integration-the-basics/supporting-instant-distributions",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/gating-with-superfluid-subscriptions-and-guild.xyz",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/displaying-token-balances",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/useful-queries-for-your-integration",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/useful-queries-for-your-integration/instant-distribution-events",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/useful-queries-for-your-integration/money-streaming-events",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/useful-queries-for-your-integration/super-token-events",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/useful-queries-for-your-integration/other-helpful-queries",
                "https://docs.superfluid.finance/superfluid/developers/integration-guides/constructing-links-to-the-superfluid-dashboard",
                "https://docs.superfluid.finance/superfluid/developers/superfluid-subscriptions",
                "https://docs.superfluid.finance/superfluid/developers/superfluid-subscriptions/superfluid-checkout-widget",
                "https://docs.superfluid.finance/superfluid/developers/superfluid-subscriptions/implementing-subscriptions-in-your-app",
                "https://docs.superfluid.finance/superfluid/developers/sdk-core",
                "https://docs.superfluid.finance/superfluid/developers/sdk-core/sdk-core-initialization",
                "https://docs.superfluid.finance/superfluid/developers/sdk-core/functionality",
                "https://docs.superfluid.finance/superfluid/developers/sdk-core/getting-data",
                "https://docs.superfluid.finance/superfluid/developers/sdk-core/resolver",
                # ADD REFERENCE DOC LINKS
                "https://docs.superfluid.finance/superfluid/developers/solidity-examples",
                "https://docs.superfluid.finance/superfluid/developers/solidity-examples/interacting-with-superfluid-smart-contracts",
                "https://docs.superfluid.finance/superfluid/developers/solidity-examples/libraries",
                "https://docs.superfluid.finance/superfluid/developers/solidity-examples/resolver",
                "https://docs.superfluid.finance/superfluid/developers/testing-guide",
                "https://docs.superfluid.finance/superfluid/developers/testing-guide/hardhat-testing",
                "https://docs.superfluid.finance/superfluid/developers/testing-guide/foundry-testing",
                "https://docs.superfluid.finance/superfluid/developers/testing-guide/in-depth",
                "https://docs.superfluid.finance/superfluid/developers/testing-guide/in-depth/hardhat-mainnet-fork-testing",
                "https://docs.superfluid.finance/superfluid/developers/testing-guide/in-depth/super-app-testing-on-mainnet-forks",
                "https://docs.superfluid.finance/superfluid/developers/subgraph",
                "https://docs.superfluid.finance/superfluid/developers/reference-documentations/production-deployment",
                "https://docs.superfluid.finance/superfluid/developers/networks",
                ]
    
def getss(url_to_scrape, service):
    index = 1
    # TODO -> HANDLE MEMORY
    for url in url_to_scrape:
        print("HANDLING FILE: ", index)
        os.makedirs('{}/page_{}'.format(service,index), exist_ok=True)
        driver.get(url)

        web_page_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
        
        temp = 0
        mini_idx = 0
        while temp <= web_page_height:
            driver.execute_script("window.scrollTo(0, {});".format(temp))
            
            # take screenshot of current view
            driver.set_window_size(1496, 680);
            driver.get_screenshot_as_file('web_page_{}_{}.png'.format(index,mini_idx))
            im = Image.open('web_page_{}_{}.png'.format(index,mini_idx))
            im1 = im.crop((292, 80, 1180, 680))
            im1.save('{}/page_{}/ss_{}_{}.png'.format(service,index,index,mini_idx))
            mini_idx += 1
            temp += 600
        index += 1


# todo -> optimize this
def process_images_to_pdf(service, urls):
    images = []
    idx = 0
    page_num = 1
    json_map = {}
    
    for folder in os.listdir(service):
        link = urls[idx]
        for image in os.listdir('{}/{}'.format(service,folder)):
            json_map[str(page_num)] = link
            images.append(Image.open('{}/{}/{}'.format(service,folder,image)).convert('RGB'))
            page_num += 1
        idx += 1

    json_link_path = "linkspage.json"
    pdf_path = '{}.pdf'.format(service)

    with open(json_link_path, 'w') as outfile:
        json.dump(json_map, outfile)
        
    images[0].save(pdf_path, resolution=100.0, save_all=True, append_images=images)
    

# getss(SUPERFLUID_DEV_URLS, "superfluid")
process_images_to_pdf("superfluid", SUPERFLUID_DEV_URLS)