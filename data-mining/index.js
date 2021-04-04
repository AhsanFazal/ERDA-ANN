// USER CONFIG
const amountOfPagesToScrape = 22 // 22*48 = 1056 images

// Imports
const puppeteer = require("puppeteer")
const $ = require("cheerio")
const uuid = require("uuid")
const fetch = require("node-fetch")
const fs = require("fs")
const cliProgress = require("cli-progress")

// Function to save files to disk
async function saveImageToDisk(url, filename) {
  await fetch(url)
    .then((res) => {
      const dest = fs.createWriteStream(filename)
      res.body.pipe(dest)
    })
    .catch((err) => {
      console.log(err)
    })
}

// Page scraping function
const scrapePage = async (pageNumber = 0) => {
  const browser = await puppeteer.launch()
  const page = await browser.newPage()
  // Go to the page
  await page.goto(
    `https://` +
      `www.planespotters.net` +
      `/photos/airport/Amsterdam-Schiphol-AMS-EHAM?page=${pageNumber}`
  )

  const html = await page.evaluate(() => document.querySelector("*").outerHTML)

  let array = []

  $(".photo_card", html).each(function () {
    // Aquire the image data
    const imageDOMElement = $(".photo_card__header", $(this))
    const image = {
      url: $("img", imageDOMElement).attr("src"),
      alt: $("img", imageDOMElement).attr("alt"),
    }
    // Aquire airplane data
    const planeDOMElement = $(".photo_card__data", $(this))
      .contents()
      .map(function () {
        return this.type === "text" && $(this).text() !== ""
          ? $(this).text().trim()
          : ""
      })
      .get()
      .filter((str) => str !== "")
    // Remove photographers credit
    planeDOMElement.shift()
    // Remove airport data
    planeDOMElement.pop()

    const carrier = planeDOMElement[0]
    const aircraftData = planeDOMElement[1].split(" ")
    const manufacturer = aircraftData.shift()
    const aircraftType = aircraftData.join(" ")
    const aircraftMainType = aircraftType.split("-").shift()

    const id = uuid.v4()

    array.push({
      fileName: `${carrier}.${manufacturer}.${aircraftMainType}.${id}.jpg`,
      aircraft: {
        manufacturer,
        detailedType: aircraftMainType,
        type: aircraftType,
      },
      carrier,
      image,
    })
  })

  browser.close()

  return array
}

// Start function
const start = async () => {
  let pages = []
  console.clear()
  const primaryProgressBar = new cliProgress.SingleBar(
    {},
    cliProgress.Presets.shades_classic
  )

  for (let i = 1; i < amountOfPagesToScrape + 1; i++) {
    console.log(`Scraping page ${i} of ${amountOfPagesToScrape}... \n`)
    primaryProgressBar.start(amountOfPagesToScrape, i)
    console.log("\n")
    // Scrape the page
    const page = await scrapePage(i)
    // Create progressbar for image downloading
    const secondaryProgressBar = new cliProgress.SingleBar(
      {},
      cliProgress.Presets.shades_classic
    )
    console.log(`Downloading images for page ${i}... \n`)
    secondaryProgressBar.start(page.length, 0)
    for (let i = 0; i < page.length; i++) {
      await saveImageToDisk(page[i].image.url, `./images/${page[i].fileName}`)
      secondaryProgressBar.update(i + 1)
    }
    secondaryProgressBar.stop()
    // Add this page to pages object
    pages = pages.concat(page)
    // Notify user of successful scrape
    console.clear()
  }
  console.log(`Done scraping ${amountOfPagesToScrape} pages! \n`)
  console.log("Writing JSON file with all image data...\n")
  // Stringify pages object and write to filesystem
  let data = JSON.stringify(pages)
  fs.writeFileSync("./imageAnnotations.json", data)
  // Notify user of success :)
  console.log(`All done :)`)
}

start()
