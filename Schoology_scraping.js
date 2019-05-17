const email = "hcps-malanis1@henricostudents.org"
const password = "Knoxfor'1jkl"
const username = "hcps-malanis1"
const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}
const puppeteer = require('puppeteer');

(async() => {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto('https://henrico.schoology.com');
        // takes you to google sign in page in guest browser
        await page.waitForSelector("input.whsOnd.zHQkBf")
        const firstlogininputs = await page.evaluate(() => {
                // clicking on the input for the email
                firstinput = document.querySelector('input.whsOnd.zHQkBf');
                firstinput.click();
            })
            //types in the email
        await page.type("input.whsOnd.zHQkBf", email);
        const firstloginnextbtn = await page.evaluate(() => {
            //clicking the next button
            firstnextbtn = document.querySelector("div.ZFr60d.CeoRYc");
            firstnextbtn.click();
        })
        try {
            // if the hcps page comes up log in
            await page.waitForSelector("input#input_1");
            const seconedlogin = await page.evaluate(() => {
                const usernamelogin = document.querySelector("input#input_1");
                //clicking the email text box
                usernamelogin.click();
            })
            await page.type("input#input_1", username);
            const firstpassinput = await page.evaluate(() => {
                const passlogin = document.querySelector("input#input_2");
                //clicking the password text box
                passlogin.click();
            })
            await page.type("input#input_2", password)
            const submitbutton = await page.evaluate(() => {
                const submitbtn = document.querySelector("input.credentials_input_submit");
                // clicking the submit button
                submitbtn.click();
            })
        } catch (err) {; }
        const overdue = await page.evaluate(() => {
            const overdueitemswrapper = document.querySelector("#right-column-inner > div.overdue-submissions.overdue-submissions-wrapper");;
            const upcomingoverduelist = overdueitemswrapper.querySelector("div.upcoming-list");
            const overdueitems = upcomingoverduelist.querySelectorAll("a");
            try {
                console.log(overdueitems);
            } catch (e) { throw e }
        })
        await sleep(50000)
        await page.screenshot({ path: 'example.png' });
        await browser.close()
    } catch (err) {
        throw err
    };

})();
