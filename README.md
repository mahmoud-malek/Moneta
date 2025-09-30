# Moneta

Moneta is a sleek, user-friendly expense tracker designed to help individuals manage their finances with ease. Built with a focus on simplicity and efficiency, Moneta offers a range of features that make tracking expenses and income straightforward and intuitive.

## Features

- **Expense and Income Tracking**: Keep tabs on your financial activity, categorize transactions, and monitor your spending habits over time.
- **Budget Setting**: Create custom budgets for different categories to ensure you stay on track with your financial goals.
- **Detailed Reports**: Gain insights into your financial health with detailed reports and visualizations of your income, expenses, and savings.
- **User-Friendly Dashboard**: Navigate through the app with ease thanks to a clean, intuitive dashboard that puts all your financial information at your fingertips.
- **Secure and Private**: Your financial data is encrypted and stored securely, ensuring your privacy and peace of mind.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Font Awesome, Google Fonts
- **Backend**: Python with Flask
- **Database**: MySQL
- **Deployment**: Ngnix, Gunicorn

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Python 3.6+
- MySQL

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/your_username_/moneta.git
   ```

2. Go to the project directory

   ```sh
   cd Moneta
   ```

3. Install dependencies

   ```sh
   pip install -r requirements.txt
   ```

4. Start the development server

   ```sh
   flask --app web.app run --debug
   ```

## Deploying on Render

Render can build and host the app as a managed web service. This repository already includes a `render.yaml` blueprint that provisions a free tier web service and a managed MySQL instance. You can deploy in just a few steps:

1. Push your code to a GitHub repository (public or private).
2. Create a Render account at [https://render.com](https://render.com) and connect it to your GitHub repository.
3. From the Render dashboard, choose **New + → Blueprint** and select this repository. Render will read `render.yaml`, create the `moneta-db` MySQL database, and set up the `moneta-web` service.
4. When prompted, review the environment variables:
   - `SECRET_KEY` is generated automatically.
   - `MONETA_DATABASE_URL` comes from the managed database connection string.
   - `MONETA_DB_DRIVER` defaults to `mysql+pymysql`.
   - You can add optional overrides (such as custom session secrets) under **Environment → Add Environment Variable**.
5. Click **Apply** to start the first deploy. Render will run `pip install -r requirements.txt` and start the app via `gunicorn wsgi:application`.

### Data Migrations

The SQLAlchemy models automatically create tables on startup. If you need sample data, you can add it through the web dashboard or run a custom script against the database using the `MONETA_DATABASE_URL` connection string.

### Running Ad-hoc Commands

For database initialization or one-off scripts, use Render Shell (available under the service’s **Shell** tab) or run a background job with the same build command and environment variables.

### Production Notes

- Store sensitive credentials (e.g., email SMTP credentials) as Render environment variables rather than hard-coding them.
- Monitor logs in the Render dashboard under **Logs**.
- Enable automatic deploys so every push to the `master` branch redeploys the service.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

## Story & Inspiration

The inspiration behind Moneta came from the need for a simple and easy-to-use expense tracker that helps people manage their finances. I Was inspired to create Moneta after struggling with Excel spreadsheets, word documents, and papers to track my expenses and income.

I wanted to create a tool that would make it easy for people to track their finances and make better financial decisions. as a result, Moneta was born. I worked on Moneta alone, and it took me about 3 weeks to design and develop the application.

I used HTML, CSS, and JavaScript for the front-end, and Python with Flask for the back-end.
I also used MySQl as the database. I chose these technologies because I am familiar with them and have experience working with them. I also wanted to keep the application simple and lightweight, so I avoided using complex frameworks and libraries.

## Screenshots

### From Web

![App Screenshot](https://i.imgur.com/LrIeMNe.png)

### From Phone

![App Screenshot](https://imgur.com/Ha2WnGD.png)

## Authors

- [@mahmoud-malek](https://www.github.com/mahmoud-malek)
