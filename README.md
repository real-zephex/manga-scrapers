# Manga Scraper API [under development]

This is a FastAPI-based web application for scraping manga information from various sources including Manganato, Mangareader, Mangapill, and Asurascans.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/real-zephex/Dramalama.git
    cd Dramalama
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Homepage
- **GET /**: Welcome message.
  ```json
  {
      "message": "Welcome to the manganato scraper"
  }

## Sources Supported
1. [Manganato](https://manganato.com/)
2. [Mangareader](https://mangareader.tv/)
3. [Mangapill](https://mangapill.com/)
4. [Asurascans](https://asurascans.io/) - not working on demo site, works when hosted locally (help needed)
5. [Flamecomics](https://flamecomics.me/)


### Manganato
- **GET /manganato/search/{path}**: Search manga by query.
- **GET /manganato/info/{path}**: Get manga info by ID.
- **GET /manganato/pages/{path}**: Get manga pages by ID.
- **GET /manganato/latest/{path}**: Get the latest manga (with optional page number).
- **GET /manganato/newest/{path}**: Get the newest manga (with optional page number).
- **GET /manganato/hotest/{path}**: Get the hottest manga (with optional page number).
- **GET /manganato/image/{path}**: Get the manga image by URL.

### Mangareader
- **GET /mangareader/search/{path}**: Search manga by query.
- **GET /mangareader/info/{path}**: Get manga info by ID.
- **GET /mangareader/pages/{path}**: Get manga pages by ID.
- **GET /mangareader/genre-list**: Get the list of genres.
- **GET /mangareader/latest/{path}**: Get the latest manga by genre.

### Mangapill
- **GET /mangapill/search/{path}**: Search manga by query.
- **GET /mangapill/info/{path}**: Get manga info by ID.
- **GET /mangapill/pages/{path}**: Get manga pages by ID.
- **GET /mangapill/newest**: Get the newest manga.
- **GET /mangapill/images/{path}**: Get the manga image by URL.

### Asurascans
- **GET /asurascans/search/{path}**: Search manga by query.
- **GET /asurascans/info/{path}**: Get manga info by ID.
- **GET /asurascans/pages/{path}**: Get manga pages by ID.
- **GET /asurascans/popular**: Get the popular manga.
- **GET /asurascans/latest/{path}**: Get the latest manga (with optional page number).
- **GET /asurascans/genres/{path}**: Get manga by genre type.
- **GET /asurascans/genre-list**: Get the list of genres.

### Flamecomics
- **GET /flamescans/search/{path}**: Search manga by title
- **GET /flamescans/info/{path}**: Get manga info by ID.
- **GET /flamescans/pages/{path}**: Get manga pages by ID.
- **GET /flamescans/sort/{path}**: Get the popular manga. Accepts `title`, `titlereverse`, `update`, `popular`, `added`

## Example Queries

- **Manganato Search**: `GET /manganato/search/one_piece`
- **Mangareader Latest by Genre**: `GET /mangareader/latest/Action`
- **Mangapill Newest**: `GET /mangapill/newest`
- **Asurascans Popular**: `GET /asurascans/popular`

## Note
For image retrieval endpoints, appropriate headers are set to ensure the correct referer is used to avoid access issues.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
