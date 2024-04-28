import { Builder, By, Key, until, Condition } from "selenium-webdriver";
import { assert } from "chai";

async function getDriver() {
  const host = process.env.SELENIUM || "selenium";
  return await new Builder()
    .usingServer(`http://${host}:4444`)
    .forBrowser("chrome")
    .build();
}

until.elementIsNotPresent = function elementIsNotPresent(locator) {
  return new Condition(
    "for no element to be located " + locator,
    async function (driver) {
      const elements = await driver.findElements(locator);
      return elements.length === 0;
    }
  );
};

describe("chat", async function () {
  let driver;

  beforeEach(async function () {
    driver = getDriver();
  });

  afterEach(async function () {
    if (driver) {
      await driver.quit();
    }
  });

  const messageSelector = By.css("[data-testid=stChatMessage]");
  const textAreaSelector = By.css("[data-testid=stChatInputTextArea]");

  it("should show greeting message", async function () {
    await driver.get("https://statham.ebo.sh/");
    await driver.wait(until.elementLocated(textAreaSelector), 3000);

    const chatMessage = await driver.findElement(messageSelector);
    const messageText = await chatMessage.getText();

    assert.isTrue(messageText == "How can I help you?");
  });

  it("should send user message", async function () {
    await driver.get("https://statham.ebo.sh/");
    await driver.wait(until.elementLocated(textAreaSelector), 3000);

    const userMessage = "Hello, tell me funny story";

    const textArea = await driver.findElement(textAreaSelector);
    await textArea.sendKeys(userMessage, Key.ENTER);

    await driver.wait(async function (driver) {
      const elements = await driver.findElements(messageSelector);
      return elements.length >= 2;
    }, 3000);

    const chatMessages = await driver.findElements(messageSelector);

    const messageText = await chatMessages[1].getText();

    assert.isTrue(messageText == userMessage);
  });

  it("should response with message", async function () {
    await driver.get("https://statham.ebo.sh/");
    await driver.wait(until.elementLocated(textAreaSelector), 3000);

    const userMessage = "Hello, tell me funny story";

    const textArea = await driver.findElement(textAreaSelector);
    await textArea.sendKeys(userMessage, Key.ENTER);

    await driver.wait(async function (driver) {
      const elements = await driver.findElements(messageSelector);
      return elements.length == 3;
    }, 3000);

    await driver.wait(async function (driver) {
      const elements = await driver.findElements(messageSelector);
      return (await elements[2].getText()).length > 0;
    }, 3000);

    const chatMessages = await driver.findElements(messageSelector);

    const messageText = await chatMessages[2].getText();

    assert.isTrue(messageText.length > 0);
  });
});

describe("favorites", async function () {
  let driver;

  beforeEach(async function () {
    driver = getDriver();
  });

  afterEach(async function () {
    if (driver) {
      await driver.quit();
    }
  });

  const messageSelector = By.css("[data-testid=stChatMessage]");
  const textAreaSelector = By.css("[data-testid=stChatInputTextArea]");

  it("should add response to favorites", async function () {
    await driver.get("https://statham.ebo.sh/");
    await driver.wait(until.elementLocated(textAreaSelector), 3000);

    const userMessage = "Hello, tell me funny story";

    const textArea = await driver.findElement(textAreaSelector);
    await textArea.sendKeys(userMessage, Key.ENTER);

    await driver.wait(async function (driver) {
      const elements = await driver.findElements(messageSelector);
      return elements.length == 3;
    }, 3000);

    const chatMessages = await driver.findElements(messageSelector);
    const responseMessage = chatMessages[2];

    await driver.wait(async function (driver) {
      const elements = await driver.findElements(messageSelector);
      try {
        const button = await elements[2].findElement(
          By.css("[data-testid=stButton]")
        );
        return button != null;
      } catch {
        return false;
      }
    }, 5000);

    const saveButton = await responseMessage.findElement(
      By.css("[data-testid=stButton] > button")
    );

    await saveButton.click();

    await driver.wait(
      until.elementLocated(By.css("[data-testid=stToast]")),
      3000
    );
    const toast = await driver.findElement(By.css("[data-testid=stToast]"));
    const toastText = await toast.getText();

    assert.isTrue(toastText == "❤️ Response saved to favorites!");

    await driver.wait(
      until.elementIsNotPresent(By.css("[data-testid=stButton]")),
      3000
    );
  });

  it("should show saved in favorites", async function () {
    await driver.get("https://statham.ebo.sh/");
    await driver.wait(until.elementLocated(textAreaSelector), 3000);

    const userMessage = "Hello, tell me funny story";

    const textArea = await driver.findElement(textAreaSelector);
    await textArea.sendKeys(userMessage, Key.ENTER);

    await driver.wait(async function (driver) {
      const elements = await driver.findElements(messageSelector);
      return elements.length == 3;
    }, 3000);

    const chatMessages = await driver.findElements(messageSelector);
    const responseMessage = chatMessages[2];

    await driver.wait(async function (driver) {
      const elements = await driver.findElements(messageSelector);
      try {
        const button = await elements[2].findElement(
          By.css("[data-testid=stButton]")
        );
        return button != null;
      } catch {
        return false;
      }
    }, 5000);

    const saveButton = await responseMessage.findElement(
      By.css("[data-testid=stButton] > button")
    );
    await saveButton.click();

    await driver.wait(
      until.elementIsNotPresent(By.css("[data-testid=stButton]")),
      3000
    );

    const savedText = await responseMessage.getText();

    // await driver.navigate().to("https://statham.ebo.sh/Favorites");
    const menuLinks = await driver.findElements(
      By.css("[data-testid=stSidebarNavLink]")
    );
    const favoritesLink = menuLinks[1];
    await favoritesLink.click();

    await driver.wait(until.urlContains("Favorites"));

    await driver.wait(until.elementLocated(messageSelector), 3000);

    await driver.wait(async function (driver) {
      const element = await driver.findElement(messageSelector);
      const messageText = await element.getText();

      return messageText == savedText;
    }, 5000);
  });
});
