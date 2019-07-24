const puppeteer = require('puppeteer');

// // run: "node google.test.js" with the below to see the browser come up.
// (async () => {
//   const browser = await puppeteer.launch({
//     headless: false,
//     slowMo: 500,
//     devtools: true
//   });
//   const page = await browser.newPage();
//   await page.goto('https://google.com');

//   await browser.close();
// })();

// describe('Google', () => {
//   beforeAll(async () => {
//     await page.goto('https://google.com');
//     // await page.screenshot({ path: 'google.png'})
//   });

//   it('should display "google" text on page', async () => {
//     await expect(page).toMatch('google');
//   });
// });



// (async () => {
//   const browser = await puppeteer.launch({
//     headless: false,
//     slowMo: 500,
//     devtools: true
//   });
//   const page = await browser.newPage();
//   await page.goto('http://192.168.33.10/admin');

//   await browser.close();
// })();


describe('Admin', () => {
  beforeAll(async () => {
    // const page = await browser.newPage();
    await page.goto('http://192.168.33.10/admin');
    await page.type('#id_username', 'admin');
    await page.type('#id_password', 'development');
    await page.click('[type=submit]');
  });
  it('tests that the admin can login', async () => {
    var title = await page.title();
    await expect(title).toMatch("Site administration | Django site admin");
  });
});

describe('New Projects', () => {
  // it('tests that not logged in users cannot add new projects', async () => {
  //   var content = await page.content();
  //   await page.goto('http://192.168.33.10/');
  //   await expect(content).not.toMatch("Add New Project");
  // })
  beforeAll(async () => {
    // const page = await browser.newPage();
    // var content = await page.content();
    // await page.goto('http://192.168.33.10/');
    // await expect(content).not.toMatch("Add New Project");

    await page.goto('http://192.168.33.10/user/login');
    await page.type('[type=text]', 'admin');
    await page.type('[type=password]', 'development');
    await page.click('[type=submit]');
    await page.waitForNavigation();
    // console.log(page);
    // await page.screenshx§ot({ path: 'google.png'});
  });
  it('tests that logged users can add new projects', async () => {
    // console.log(page);
    var content = await page.content();
    // console.log(content);
    await expect(content).toMatch("Add New Project");
  });
});