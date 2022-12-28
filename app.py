import os

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

# Connection details for the PostgreSQL database
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "ratestask")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")


@app.route('/rates', methods=['GET'])
def get_rates():
    "GET API to fetch rates based on date and location"
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    if not date_from or not date_to or not origin or not destination:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        c = conn.cursor()

        # Query the database to get the average prices for each day on the specified route
        query = '''
            SELECT TO_CHAR(days.day, 'YYYY-MM-DD') as day, COALESCE(AVG(prices.price), null) as average_price
            FROM (
                SELECT day
                FROM prices
                WHERE day BETWEEN %s AND %s
                AND (orig_code = %s OR orig_code IN (SELECT code FROM ports WHERE parent_slug = %s))
                AND (dest_code = %s OR dest_code IN (SELECT code FROM ports WHERE parent_slug = %s))
                GROUP BY day
                HAVING COUNT(*) >= 3
            ) as days
            LEFT JOIN prices ON days.day = prices.day
            AND (prices.orig_code = %s OR prices.orig_code IN (SELECT code FROM ports WHERE parent_slug = %s))
            AND (prices.dest_code = %s OR prices.dest_code IN (SELECT code FROM ports WHERE parent_slug = %s))
            GROUP BY days.day
        '''

        c.execute(query, (date_from, date_to, origin, origin, destination,
                  destination, origin, origin, destination, destination))
        rows = c.fetchall()
        results = []
        for row in rows:
            day, average_price = row
            results.append({'day': day, 'average_price': int(average_price)})

        return jsonify(results)
    except psycopg2.Error as error:
        return jsonify({'error': str(error)}), 500
    finally:
        c.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=1300)
