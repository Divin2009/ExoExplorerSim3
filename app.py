from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__, static_url_path='/static')

def is_in_habitable_zone(star_type, distance):
    habitable_zones = {
        'G': (0.95, 1.37),  # G-type stars
        'K': (0.85, 1.50),  # K-type stars
        'M': (0.30, 0.80)   # M-type stars
    }
   
    if star_type not in habitable_zones:
        return None, "Invalid star type. Please enter 'G', 'K', or 'M'."
    min_distance, max_distance = habitable_zones[star_type]
    if min_distance <= distance <= max_distance:
        return True, "The exoplanet is in the habitable zone."
    else:
        return False, "The exoplanet is not in the habitable zone."

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_habitable_zone():
    star_type = request.form['star_type'].strip().upper()
    try:
        distance = float(request.form['distance'])
    except ValueError:
        return render_template('error.html', error="Invalid distance. Please enter a number.")

    is_habitable, message = is_in_habitable_zone(star_type, distance)
    
    if is_habitable is None:
        return render_template('error.html', error=message)
    
    return render_template('results.html', 
                           is_habitable=is_habitable, 
                           message=message, 
                           star_type=star_type, 
                           distance=distance)

if __name__ == '__main__':
    app.run(debug=True)