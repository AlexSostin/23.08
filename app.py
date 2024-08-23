from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to get all pets from the database
def get_all_pets():
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pets')
    pets = cursor.fetchall()
    conn.close()
    pets_list = [{'id': row[0], 'name': row[1], 'age': row[2], 'picture_url': row[3]} for row in pets]
    return pets_list

# Function to get a single pet by ID from the database
def get_pet_by_id(pet_id):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pets WHERE id = ?', (pet_id,))
    pet = cursor.fetchone()
    conn.close()
    if pet:
        return {'id': pet[0], 'name': pet[1], 'age': pet[2], 'picture_url': pet[3]}
    else:
        return None

# Endpoint to get all pets (JSON response)
@app.route('/pets', methods=['GET'])
def pets_list_json():
    pets = get_all_pets()
    return jsonify(pets)

# Endpoint to get a single pet by ID (JSON response)
@app.route('/pets/<int:pet_id>', methods=['GET'])
def pet_detail_json(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet:
        return jsonify(pet)
    else:
        return jsonify({'error': 'Pet not found'}), 404

# Endpoint to add a new pet
@app.route('/pets', methods=['POST'])
def add_pet():
    new_pet = request.form.to_dict()
    # Ensure all required fields are provided
    if 'id' not in new_pet or 'name' not in new_pet or 'age' not in new_pet or 'picture_url' not in new_pet:
        return redirect(url_for('show_all_pets'))

    # Check if the pet ID already exists
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pets WHERE id = ?', (new_pet['id'],))
    existing_pet = cursor.fetchone()
    if existing_pet:
        conn.close()
        return redirect(url_for('show_all_pets'))

    cursor.execute('''
        INSERT INTO pets (id, name, age, picture_url)
        VALUES (?, ?, ?, ?)
    ''', (new_pet['id'], new_pet['name'], new_pet['age'], new_pet['picture_url']))
    conn.commit()
    conn.close()
    return redirect(url_for('show_all_pets'))

# Endpoint to update an existing pet by ID
@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet:
        updated_data = request.get_json()
        conn = sqlite3.connect('pets.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pets
            SET name = ?, age = ?, picture_url = ?
            WHERE id = ?
        ''', (updated_data.get('name', pet['name']),
              updated_data.get('age', pet['age']),
              updated_data.get('picture_url', pet['picture_url']),
              pet_id))
        conn.commit()
        conn.close()
        return jsonify({**pet, **updated_data})
    else:
        return jsonify({'error': 'Pet not found'}), 404

# Endpoint to delete a pet by ID
@app.route('/pets/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    if request.form.get('action') == 'delete':
        conn = sqlite3.connect('pets.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pets WHERE id = ?', (pet_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('show_all_pets'))

# Route to display all pets in HTML
@app.route('/')
def show_all_pets():
    pets = get_all_pets()
    return render_template('all_pets.html', pets=pets)

# Route to display a single pet's details in HTML
@app.route('/pets/<int:pet_id>/details')
def show_pet_detail(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet:
        return render_template('pet_detail.html', pet=pet)
    else:
        return render_template('error.html', message='Pet not found'), 404

# Error handling
@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', message='Bad request'), 400

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message='Not found'), 404

if __name__ == '__main__':
    app.run(debug=True)
