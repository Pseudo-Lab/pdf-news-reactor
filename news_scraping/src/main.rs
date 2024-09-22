use reqwest;
use reqwest::blocking::Client;
use scraper;
use select::document::Document;

fn scraping(url: &str) {
    let client = Client::new();
    let response = client.get(url).send();

    let data = response.unwrap().text().unwrap();
    println!("{data}");

    let html_product_selector = scraper::Selector::parse("div.col").unwrap();
    let html_products = document.select(&html_product_selector);
}

fn main() {
    scraping("https://demo.opencart.com/")
}
