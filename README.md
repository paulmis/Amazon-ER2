# Amazon Elastic Review Review (Amazon ER2)

Welcome to **Amazon Elastic Review Review**, an advanced review analyzer tailored for Amazon sellers. Our tool leverages cutting-edge technologies to identify key issues from customer feedback, cluster them for better understanding, and prioritize them based on their impact on your business.

_Note: this project is not affiliated with Amazon, and was built as a solution for a LauzHack 2023 challenge prepared by AWS._

### Key Features:
- **Issue Identification**: Extracts critical insights from reviews using advanced NLP models.
- **Clustering**: Groups similar issues using the OPTICS clustering algorithm for a clearer overview.
- **Prioritization**: Prioritizes issues based on their frequency and impact on customer satisfaction.

![image (2)](https://github.com/paulmis/lauzhack23/assets/45182027/f040a784-035b-422d-bab4-eba4f95fdf2d)


## How to run
You can run this demo locally only:

1. Install NPM and Python 3

2. Clone the repository

```
git clone https://github.com/paulmis/lauzhack23.git
```

3. Install all dependencies. For frontend:

```
cd frontend
npm i
```

For backend:
```
cd backend
python3 -m pip install -r requirements.txt
```

4. Provide credentials for an account with Amazon Bedrock's Claude v2 LLM enabled.

```
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN=
```

5. Run the backend

```
cd backend
python3 run.py
```

If successful, you should see:
```
Create new client
  Using region: us-east-1
boto3 Bedrock client successfully created!
bedrock-runtime(https://bedrock-runtime.us-east-1.amazonaws.com)
 * Serving Flask app 'api'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

6. Run the `populate_database.py` file.
This should populate the database with the provided CSV file. See section below on how to provide the data.

7. Run the frontend

```
cd frontend
npm run dev
```

If successful, you should see:
```
> my-app@0.1.0 dev
> next dev

   ▲ Next.js 14.0.3
   - Local:        http://localhost:3000

 ✓ Ready in 3.3s
```

8. Access `localhost:3000` to see the user interface.

### Provide your own dataset

To integrate your own dataset with Amazon Elastic Review Review, follow these steps:

1. Prepare your dataset in CSV format. The dataset should adhere to the following column structure:

   ```
   Product Name,Brand Name,Price,Rating,Reviews,Review Votes
   ```

   - `Product Name`: The name of the product.
   - `Brand Name`: The name of the brand associated with the product.
   - `Price`: The price of the product.
   - `Rating`: The rating out of 5 of the review.
   - `Reviews`: The text of the customer review.
   - `Review Votes`: The number of votes/likes the review received.

2. Locate the `populate_database.py` file within the project's directory.

3. Modify the `CSV_FILE` path variable in `populate_database.py` to point to your CSV file. For instance:

   ```python
   CSV_FILE = "path/to/your/dataset.csv"
   ```

   Replace `path/to/your/dataset.csv` with the actual file path of your dataset.

4. After updating the `CSV_FILE` path, the application will use your dataset for its analysis process.
5. Rerunning the `populate_database.py` should now add the new dataset to the database. 


Note: If the script has been previously ran deleting the old database would be needed.


## Technologies Used
- **Amazon Bedrock**: Robust infrastructure for scalable data processing.
- **Claude V2 LLM**: State-of-the-art language model for natural language understanding.
- **Titan Embeddings**: Powerful feature extraction for accurate text analysis.
- **Stable Diffusion Image Generation**: Generates visual representations of data trends and clusters.
- **OPTICS Clustering**: Advanced clustering algorithm for nuanced data segmentation.
