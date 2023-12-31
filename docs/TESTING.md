# TESTING

## Contents
- [Python - Flakes8 Validation](#python---flakes8-validation)
- [JavaScript Validation](#javascript-validation)
- [HTML Validation](#html-validation)
- [CSS Validation](#css-validation)
- [Lighthouse Testing](#lighthouse-testing)
- [Compatibility Testing](#compatibility-testing)
  - [Browser Compatibility](#browser-compatibility)
  - [Device Compatibility](#device-compatibility)
- [User Stories Testing](#user-stories-testing)
- [Manual Tests](#manual-tests)
- [Bugs/Issues](#bugsissues)
- [Back to README.md](../README.md#table-of-contents)


## Python - Flakes8 Validation
The Flake8 linting tool is used to identify code-quality issues and check the Python code for PEP8 requirements.

In some cases, the Flake8 validation was ignored for a specific line of code. This was done by adding a `# noqa` comment at the end of the line.

The following Flake8 errors were ignored:
- F401: Imported but unused. Added to unsused imports in files that was generated by Django, but not used in the project.
- E501: Line too long. Added to lines that was too long, but not possible to split into multiple lines, or where it would make the code less readable.
- exlude: `migrations` folders. Added to exclude the migrations folders, as they are generated by Django.

![Flake8 Validation](images/testing/flake8.png)

[Back to top](#contents)

## JavaScript Validation
The JavaScript separate files were validated using [JSHint](https://jshint.com/).

*checkout/stripe_elements.js*

![jshint_stripe_elements](images/testing/jshint_checkout.png)

*inventorize/collapse_elements.js*

![jshint_collapse_elements](images/testing/jshint_inventorize.png)

*profiles/countryfield.js*

![jshint_countryfield](images/testing/jshint_profiles.png)

*wishlist/wishlist_toggler.js*

![jshint_wishlist_toggler](images/testing/jshint_wishlist.png)

[Back to top](#contents)

## HTML Validation
The HTML markup was validated using [W3C Markup Validation Service](https://validator.w3.org/). Since the Django templating language was used, the validation was done on the public rendered HTML pages, that not required a user to be logged in.

*Home Page*

![HTML Validation Home Page](images/testing/html_validation_home.png)

*Products Page*

![HTML Validation Products Page](images/testing/html_validation_products.png)

*Product Detail Page*

![HTML Validation Product Detail Page](images/testing/html_validation_product_detail.png)

*Featured Products Page*

![HTML Validation Featured Products Page](images/testing/html_validation_featured_products.png)

*Login Page*

![HTML Validation Login Page](images/testing/html_validation_login.png)

*Register Page*

![HTML Validation Register Page](images/testing/html_validation_register.png)

*Empty Bag Page*

![HTML Validation Empty Bag Page](images/testing/html_validation_empty_bag.png)

*Contact Page*

![HTML Validation Contact Page](images/testing/html_validation_contact.png)

[Back to top](#contents)

## CSS Validation
To validate the CSS code I used the [Jigsaw](https://jigsaw.w3.org/css-validator/) css validator.

*checkout.css*

![CSS Validation Checkout](images/testing/css_validation_checkout.png)

*home.css*

There are 4 parse errors in the home.css file, since the `:has()` pseudo-class is part of a level 4 selectors draft and is not yet supported by the validator.

![CSS Validation Home](images/testing/css_validation_home.png)

*inventorize.css*

![CSS Validation Inventorize](images/testing/css_validation_inventorize.png)

*profile.css*

![CSS Validation Profile](images/testing/css_validation_profile.png)

*base.css*

![CSS Validation Base](images/testing/css_validation_base.png)

[Back to top](#contents)

## Lighthouse Testing
The [Google Lighthouse](https://developers.google.com/web/tools/lighthouse) tool was used to check the performance, accessibility, best practices, and SEO of the website. The tests were run on the deployed website.

*Home Page*

![Lighthouse Home Page](images/testing/lighthouse_home.png)

*Products Page*

<small>To enhance the performance of the products page, I plan to implement pagination to limit the number of products loaded at once. Given that the products page features various types of sorting and filtering options, which complicate the implementation of pagination, I have decided to postpone this feature to a future update.</small>

![Lighthouse Products Page](images/testing/lighthouse_products.png)

*Product Detail Page*

![Lighthouse Product Detail Page](images/testing/lighthouse_product_detail.png)

*Empty Bag Page*

![Lighthouse Empty Bag Page](images/testing/lighthouse_empty_bag.png)

*Bag Page with Products*

![Lighthouse Bag Page](images/testing/lighthouse_bag.png)

*Checkout Page*

![Lighthouse Checkout Page](images/testing/lighthouse_checkout.png)

[Back to top](#contents)

## Compatibility Testing
- ### Browser Compatibility
The website was tested on the following browsers:
- Chrome
- Firefox
- Edge

The app worked well across all browsers and discrepancies were not found.

- ### Device Compatibility
The app was tested using Google Chrome Developer Tool - Device Mode Toolbar.
Tested devices:
- MacBook Pro
- iPhone SE
- iPhone 12 Pro
- Pixel 5
- Samsung Galaxy S8+
- Samsung Galaxy S20 Ultra
- iPad Air
- iPad Mini
- Surface Pro 7
- Surface Duo
- Samsung Galaxy A51
- Nest Hub
- Nest Hub Max
- iPad
- iPadPro

Here are some screenshots of the website on iPhone 12 Pro:

*Home Page*

![iPhone 12 Pro Home Page](images/testing/iphone12_home.png)

*Profile Page*

![iPhone 12 Pro Profile Page](images/testing/iphone12_profile.png)

*Wishlist Page*

![iPhone 12 Pro Wishlist Page](images/testing/iphone12_wishlist.png)

*Products Page*

![iPhone 12 Pro Products Page](images/testing/iphone12_products.png)

*Product Detail Page*

![iPhone 12 Pro Product Detail Page](images/testing/iphone12_product_detail.png)

*Bag Page*

![iPhone 12 Pro Bag Page](images/testing/iphone12_bag.png)

*Checkout Page*

![iPhone 12 Pro Checkout Page](images/testing/iphone12_checkout.png)

[Back to top](#contents)

## User Stories Testing
##### Epic: Viewing and Navigation

| User Story | Requirements to be met | Result |
| --- | --- | --- |
| Home Page | As a Shopper, I want to be able to see a home page so that I can quickly understand the purpose of the site and learn more about the business | Home page is displayed with essential business information and site purpose. |
Navigate the site | As a Shopper, I want to be able to easily navigate throughout the site to find content so that I can find what I'm looking for efficiently | Navigation bar is displayed on all pages, and the user can easily navigate to the desired page. |
View a list of bikes | As a Shopper, I want to be able to view a list of bikes so that I can select one to purchase | List of bikes is displayed on the products page, and the user can click on a product to view the product detail page. |
View bike details | As a Shopper, I want to be able to view the details of a bike so that I can identify the price, color, type, size and image | Product detail page shows all relevant information about the product. |
Identify special offers | As a Shopper, I want to be able to quickly identify special offers so that I can take advantage of special savings | The user can see the special offers on the home page and the products page. |
View total of purchases | As a Shopper, I want to be able to easily view the total of my purchases at any time so that I can avoid spending too much | Cart shows the total cost of selected items. |
Contact via form | As a Shopper, I want to be able to contact the store owner using the contact form so that I can ask any questions I may have | Contact form is easily accessible from the navigation bar and footer and functions as intended. |

##### Epic: Registration and User Accounts

| User Story | Requirements to be met | Result |
| --- | --- | --- |
Register for an account | As a Shopper, I want to be able to easily register for an account | User can register through a simple form and receives a confirmation email. |
Login/Logout | As a Shopper, I want to be able to easily login or logout | User can login or logout |
Recover password | As a Shopper, I want to be able to easily recover my password | Password recovery option is available and sends reset instructions to the user's email. |
Receive email confirmation | As a Shopper, I want to be able to receive an email confirmation after registering | User receives a confirmation email after successful registration |


##### Epic: User Profile and Purchases

| User Story | Requirements to be met | Result |
| --- | --- | --- |
Personalized profile | As a Shopper, I want to be able to have a personalized user profile | User profile shows order history and saved payment information |
Save products for later | As a Shopper, I want to be able to save the products I want to buy later | User can add products to the wishlist from the products page|
View wishlist | As a Shopper, I want to be able to view my wish list | Wishlist is accessible and shows saved items |

##### Epic: Sorting and Searching

| User Story | Requirements to be met | Result |
| --- | --- | --- |
Sort products | As a Site User, I want to be able to sort the list of available products | Sorting options are available for price, category, brand, color and name in ascending and descending order. |
Filter products | As a Shopper, I want to be able to use filters | To be implemented in a future update. |
Search for products | As a Shopper, I want to be able to search for a product | Search bar is available and functional. |

##### Epic: Purchasing and Checkout

| User Story | Requirements to be met | Result |
| --- | --- | --- |
Select size and quantity | As a Shopper, I want to be able to easily select the size and quantity of a bike | Select size is available on the product detail page, and quantity can be selected on the bag page. |
View items in bag | As a Shopper, I want to be able to view bikes in my bag | User can view items and total cost in the shopping bag |
Adjust quantity in bag | As a Shopper, I want to be able to adjust the quantity of individual items in my bag | Option to adjust quantity for items in the shopping bag is available and valid. |
Remove items from bag | As a Shopper, I want to be able to remove a bike from my bag | Option to remove items from the shopping bag is available and valid. |
Enter payment information | As a Shopper, I want to be able to easily enter my payment information | Payment form is user-friendly and accepts all necessary information |
Feel information is secure | As a Shopper, I want to be able to feel my personal and payment information is safe | Payment is processed using Stripe, and the user can feel confident that their information is secure. |
View order confirmation | As a Shopper, I want to be able to view an order confirmation after checkout | User is directed to an order confirmation page after successful payment |
Receive email confirmation | As a Shopper, I want to be able to receive an email confirmation after checking out | User receives an order confirmation email after successful payment. |


##### Epic: Newsletters and Social Media

| User Story | Requirements to be met | Result |
| --- | --- | --- |
Subscribe to a Newsletter | As a Shopper, I want to be able to subscribe to a Newsletter | Newsletter subscription form is available and functional. |
Send Newsletter | As a Store Owner, I want to be able to send a newsletter to subscribers | Newsletter can be sent to all subscribers through the mailchimp account. |
Facebook page | As a Store Owner, I need a Facebook page to promote my business | Facebook page for the store is set up and active |

##### Epic: Store Management

| User Story | Requirements to be met | Result |
| --- | --- | --- |
Add a product | As a Store Owner, I want to be able to add a product to the store | Interface for adding new products is available and functional |
Edit a product | As a Store Owner, I want to be able to edit/update a product | Options for editing existing products are available and functional |
Delete a product | As a Store Owner, I want to be able to delete a product | Option to delete a product is available and functional |
Add a category | As a Store Owner, I want to be able to add a product category | Interface for adding new categories is available and functional |
Add a brand | As a Store Owner, I want to be able to add a product brand | Interface for adding new brands is available and functional |
Add a color | As a Store Owner, I want to be able to add a product color | Interface for adding new colors is available and functional |

[Back to top](#contents)

## Manual Tests
Manual testing was performed to ensure that all features work as intended.

- All pages on the site reached by links from another findable page.

- All external links open in a new tab with rel="noopener" and target="_blank" attributes.

- Forms are validated with client-side and server-side validation. Error messages are displayed if invalid data is entered.

- User feedback are all evident in the code and the working application. Toast messages are displayed when it's appropriate.

- Payments work as expected. Stripe webhooks are received and processed correctly, even if the user accidentally closes the browser before the payment is confirmed.


## Bugs/Issues
- #### Checkout
    - **Issue:** The backend form validation executes using *stripe_elements.js* after the Stripe payment is confirmed. This means that if the form is invalid, the user will still be charged for the order.
    - **Solution:** The form validation is done on the frontend using JavaScript. If the form is invalid, the user will be notified and the payment will not be processed.
    - **Future Update:** The functionality will be completely refactored to use the Django forms validation before the payment is processed, to ensure that the user cannot bypass the frontend validation.

- #### Products
    - **Issue:** The performance of the products page is not optimal. The page loads all product images at once, which can cause a delay in loading the page.
    - **Solution:** Lazy Loading Images with Intersection Observer. As images are only loaded as they are about to be displayed, the initial page load is much faster.

[Back to README.md](../README.md#table-of-contents)