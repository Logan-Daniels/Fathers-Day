import PIL.Image
from PIL import ExifTags
import streamlit as st
import os
import random
import time
from streamlit_js_eval import streamlit_js_eval
import PIL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

st.set_page_config(page_title="Father's Day", layout="wide")

def fix_image_orientation(image):
    """
    Fix image orientation based on EXIF data
    """
    try:
        # Get EXIF data
        exif = image._getexif()
        if exif is not None:
            # Find orientation tag (274 is the EXIF tag number for orientation)
            orientation_key = None
            for key, value in ExifTags.TAGS.items():
                if value == 'Orientation':
                    orientation_key = key
                    break
            
            if orientation_key is None:
                # Fallback to the standard orientation tag number
                orientation_key = 274
            
            # Get orientation value
            orientation = exif.get(orientation_key)
            
            # Apply rotation based on orientation
            if orientation == 2:
                # Horizontal flip
                image = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                # 180 degree rotation
                image = image.rotate(180, expand=True)
            elif orientation == 4:
                # Vertical flip
                image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                # Horizontal flip + 90 degree rotation
                image = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                image = image.rotate(90, expand=True)
            elif orientation == 6:
                # 90 degree clockwise rotation
                image = image.rotate(-90, expand=True)
            elif orientation == 7:
                # Horizontal flip + 270 degree rotation
                image = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                image = image.rotate(-90, expand=True)
            elif orientation == 8:
                # 90 degree counter-clockwise rotation
                image = image.rotate(90, expand=True)
                
    except (AttributeError, KeyError, TypeError):
        # No EXIF data or no orientation tag
        pass
    
    return image

def send_email(selections):
    email = st.secrets["email"]
    sender_password = st.secrets["email_password"]

    # Create message
    message = MIMEMultipart()
    message["From"] = email
    message["To"] = email
    message["Subject"] = f"Father's Day Menu Selection - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # Create email body
    body = "Father's Day Menu Selections:\n\n"
    
    for item, selected in selections.items():
        if selected:
            if item == "coke_type":
                body += f"• Coke Zero ({selected})\n"
            elif item == "shopping":
                body += f"• Shopping request: {selected}\n"
            elif item == "requests":
                body += f"• Other requests: {selected}\n"
            elif item == "bagel_toppings":
                body += f"• Bagel toppings: {selected}\n"
            elif item == "activity":
                body += f"• Quality time activity: {selected}\n"
            else:
                body += f"• {item}\n"
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(email, sender_password)
        text = message.as_string()
        server.sendmail(email, email, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

# Get screen height - this will be None on first run, then populated
screen_height = streamlit_js_eval(js_expressions='screen.height', key='SCR')

# Only initialize screen_height in session state if we have a valid value
if screen_height is not None and "screen_height" not in st.session_state:
    st.session_state.screen_height = screen_height

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 1

if "photos" not in st.session_state:
    st.session_state.photos = os.listdir("photos")
    st.session_state.photos = [photo for photo in st.session_state.photos if photo.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(st.session_state.photos)

if "photo_index" not in st.session_state:
    st.session_state.photo_index = 0

if "auto_play" not in st.session_state:
    st.session_state.auto_play = True

if st.session_state.photos and "screen_height" in st.session_state:

    if st.session_state.page == 1:
        new_col1, new_col2 = st.columns((3, 2))
    else:
        new_col1, new_col2 = st.columns((2, 3))
    with new_col1:
        if st.session_state.page == 1:
            st.title("Happy Father's Day Dad!")
            st.write("Dear Dad,")
            st.write("While I entirely intend on reminding you with this card of sorts how much I love and appreciate you, like I do every year, I also want to acknowledge that, much like a seder, this father's is (a little bit) different from all other father's days. You've stepped up big time in the last few months not only helping me to process Mum's passing but supporting me through my tough times since then. I've always appreciated how much you care about me and my siblings, but this year I think you've been put to the test more than ever, and you've truly proven that you are the best dad I could ever ask for. I'm so grateful that you've been there for me through the hard times and cultivated so many fantastic times which clog up my memory so much that I can hardly remember the bad times. You've always been caring, considerate, and loving, but what I've appreciated most this year is your willingness to improve yourself for our sake. I know that I can be quite frustrating at times, but you always make the effort to understand my perspective and are generous with both your belief in me and your willingness to allow me to redeem myself. I don't know how I could possibly express how appreciative I am for that. I love you so much Dad, so I decided to give you a menu of on demand coupons for today (or in future really) and this slideshow as a miniscule token of my appreciation. Have a fantastic Father's Day!!!")
            st.write("Love,")
            st.write("Logan")
            if st.button("Continue"):
                st.session_state.page = 2
                st.rerun()
        else:
            st.title("Father's Day Menu:")
            
            checkbox_col1, checkbox_col2 = st.columns(2)
            with checkbox_col1:
                french_toast = st.checkbox("French Toast")
                blueberries = st.checkbox("Blueberries")
                hug = st.checkbox("Hug")
                love = st.checkbox("Reminder that I love you")
                coke = st.checkbox("Coke Zero")
                caffeine = None
                if coke:
                    caffeine = st.radio("Caffeine", ("Caffeine Free", "Regular"), label_visibility = "collapsed", horizontal = True)
                quality_time = st.checkbox("Quality time")
                if quality_time:
                    st.text_input("Activity", placeholder = "What would you like to do?", label_visibility = "collapsed")
            with checkbox_col2:
                spinach = st.checkbox("Bowl of Spinach")
                popcorn = st.checkbox("Popcorn")
                water = st.checkbox("Water from your ridiculous filter")
                massage = st.checkbox("Massage avoiding your shingles shot arm")
                bagel = st.checkbox("Bagel")
                if bagel:
                    st.text_input("Toppings:", placeholder = "Cream cheese, margarine, etc.")
            shopping = st.text_input("Anything you want me to go shopping for", placeholder = "Bagels, Star Trek DVDs, etc.")
            requests = st.text_input("Any other requests you have for me", placeholder = "Snuggles, watching a movie, etc.")
                
            button_col1, button_col2, button_col3 = st.columns((11, 20, 30))
            with button_col1:
                if st.button("Submit"):
                    # Collect all selections
                    selections = {
                        "French toast": french_toast,
                        "Bowl of spinach": spinach,
                        "Blueberries": blueberries,
                        "Hug": hug,
                        "Popcorn": popcorn,
                        "Water": water,
                        "Reminder that I love him": love,
                        "Massage avoiding shingles shot arm": massage,
                        "coke_type": caffeine if coke else False,
                        "shopping": shopping if shopping.strip() else False
                    }
                    
                    # Send email
                    if send_email(selections):
                        st.success("Menu selections sent successfully! 🎉")
                    else:
                        st.error("Failed to send menu selections. Please try again.")
            with button_col2:
                if st.button("Back to note"):
                    st.session_state.page = 1
                    st.rerun()

    with new_col2:
        # Navigation buttons
        if st.session_state.page == 1:
            col1, col2, col3, col4 = st.columns((1.3, 1, 2, 2))
        else:
            col1, col2, col3, col4 = st.columns((1.3, 1, 2, 5))

        with col1:
            if st.button("Previous"):
                if st.session_state.photo_index > 0:
                    st.session_state.photo_index -= 1
                else:
                    st.session_state.photo_index = len(st.session_state.photos) - 1
                st.rerun()

        with col2:
            if st.button("Next"):
                if st.session_state.photo_index < len(st.session_state.photos) - 1:
                    st.session_state.photo_index += 1
                else:
                    st.session_state.photo_index = 0
                st.rerun()

        with col3:
            if st.button("Play" if not st.session_state.auto_play else "Pause"):
                st.session_state.auto_play = not st.session_state.auto_play
                st.rerun()

        # Load and process image with EXIF orientation
        image = PIL.Image.open("photos/" + st.session_state.photos[st.session_state.photo_index])
        
        # Fix orientation based on EXIF data
        image = fix_image_orientation(image)
        
        # Resize image
        width, height = image.size
        new_height = int(st.session_state.screen_height * 0.5)
        new_width = int((new_height / height) * width)
        image = image.resize((new_width, new_height), PIL.Image.LANCZOS)
        st.image(image)

    # Auto-play functionality
    if st.session_state.auto_play:
        time.sleep(3)
        if st.session_state.photo_index < len(st.session_state.photos) - 1:
            st.session_state.photo_index += 1
        else:
            st.session_state.photo_index = 0
        st.rerun()

    # Display current photo info
    #st.write(f"Photo {st.session_state.photo_index + 1} of {len(st.session_state.photos)}: {st.session_state.photos[st.session_state.photo_index]}")

elif st.session_state.photos:
    st.write("Loading screen dimensions...")
    # Also fix orientation for the loading image
    image = PIL.Image.open("photos/" + st.session_state.photos[st.session_state.photo_index])
    image = fix_image_orientation(image)
    st.image(image, width=800)

else:
    st.write("No photos found in the 'photos' directory.")