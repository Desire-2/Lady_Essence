from flask import request
from services import (
    calculate_cycle_dates, fetch_nutrition_guidance, get_nutrition_guidance,
    save_meal, get_meal_history, send_sms, send_email, schedule_appointment,
    get_health_tips, get_emergency_contacts
)
from database import (
    save_parent, save_child, get_children, update_account, delete_account,
    delete_child, authenticate_user, submit_feedback, register_user, get_user_profile, check_password_hash
)
from datetime import datetime

# Language translations
LANGUAGES = {
    'rw': {
        'welcome': "Murakaza neza muri Sisitemu (<b>Lady’s Essence</b>)\n1. Ndi Umubyeyi\n2. Ndi Umwangavu\n3. Ndatwite\n4. Ndashaka kuvugana na muganga\n5. Nahuye nihohoterwa\n6. Inama ku buzima\n7. Kwiyandikisha",
        'parent_main_menu': "Murakaza neza ku rubuga rw'ababyeyi:\n1. Ndi mushya kurubuga\n2. Nsanzwe mfite konti\n3.",
        'parent_menu': "Murakaza neza ku rubuga rw'ababyeyi:\n1. Gukurikirana igihe cy'ukwezi kwanjye\n2. Gukurikirana igihe cy'ukwezi cy'abana banjye\n3. Kwayandikisha umwana/Anana\n4. Kuvugurura konti yanjye\n5. Gusiba konti\n6. Gusiba umwana\n7. Gutanga ibitekerezo\n8. Gahunda y'ubuzima",
        'teen_menu': "Murakaza neza ku rubuga rw'abangavu:\n1. Gukurikirana igihe cy'ukwezi kwanjye\n2. Kugisha inama ku mirire n'ubuzima\n3. Gutanga ibitekerezo\n4. Gahunda y'ubuzima",
        'pregnant_menu': "Murakaza neza ku rubuga rw'abatwite:\n1. Gushaka ubufasha mumirire\n2. Gutanga ibitekerezo\n3. Gahunda y'ubuzima",
        'doctor_menu': "Murakaza neza ku rubuga rw'abaganga:\n1. Kugisha inama\n2. Nkeneye ubufasha bwihutirwa\n3. Gutanga ibitekerezo\n4. Gahunda y'ubuzima",
        'violence_menu': "Niba Wahuye nihohoterwa hamagara\n Kubuntu(Nimero iticyurwa ariyo): <b>3029<b> \n Cyangwa nimero isanzwe ariyo: <b>0788267884/ \n 0782797015 <b>\n Ushobora no kutwoherereza ubutumwa ukoresheje Email ariyo: <b>francoiseuwamriya050@gmail.com<b>",
        'health_tips': "Inama ku buzima:\n1. Mirire myiza\n2. Korera mu minsi y'ukwezi\n3. Tekereza kubuzima bw'ubwonko\n4. Subira inyuma",
        'feedback': "Murakoze gutanga ibitekerezo byanyu. Turabyifashisha kubaka sisitemu nziza."
    },
    'en': {
        'welcome': "Welcome to Lady’s Essence System\n1. I am a Parent\n2. I am a Teenager\n3. I am Pregnant\n4. I want to talk to a doctor\n5. I have experienced violence\n6. Health Tips\n7. Register",
        'parent_menu': "Welcome to the Parents' Portal:\n1. Track my menstrual cycle\n2. Track my children's cycles\n3. Register a child\n4. Update my account\n5. Delete my account\n6. Delete a child\n7. Submit feedback\n8. Health Tips",
        'teen_menu': "Welcome to the Teenagers' Portal:\n1. Track my menstrual cycle\n2. Get nutrition and health advice\n3. Submit feedback\n4. Health Tips",
        'pregnant_menu': "Welcome to the Pregnant Women's Portal:\n1. Get nutrition assistance\n2. Submit feedback\n3. Health Tips",
        'doctor_menu': "Welcome to the Doctors' Portal:\n1. Get advice\n2. I need urgent assistance\n3. Submit feedback\n4. Health Tips",
        'violence_menu': "If you have experienced violence, call:\n Kubuntu (Toll-free): <b>3029<b> \n Or regular numbers: <b>0788267884/ \n 0782797015 <b>\n You can also send an email to: <b>francoiseuwamriya050@gmail.com<b>",
        'health_tips': "Health Tips:\n1. Eat a balanced diet\n2. Exercise during your period\n3. Take care of your mental health\n4. Go back",
        'feedback': "Thank you for your feedback. We use it to improve the system."
    },
    'fr': {
        'welcome': "Bienvenue dans le système Lady’s Essence\n1. Je suis un parent\n2. Je suis un adolescent\n3. Je suis enceinte\n4. Je veux parler à un médecin\n5. J'ai subi des violences\n6. Conseils de santé\n7. S'inscrire",
        'parent_menu': "Bienvenue sur le portail des parents:\n1. Suivre mon cycle menstruel\n2. Suivre les cycles de mes enfants\n3. Enregistrer un enfant\n4. Mettre à jour mon compte\n5. Supprimer mon compte\n6. Supprimer un enfant\n7. Soumettre des commentaires\n8. Conseils de santé",
        'teen_menu': "Bienvenue sur le portail des adolescents:\n1. Suivre mon cycle menstruel\n2. Obtenir des conseils sur la nutrition et la santé\n3. Soumettre des commentaires\n4. Conseils de santé",
        'pregnant_menu': "Bienvenue sur le portail des femmes enceintes:\n1. Obtenir de l'aide pour la nutrition\n2. Soumettre des commentaires\n3. Conseils de santé",
        'doctor_menu': "Bienvenue sur le portail des médecins:\n1. Obtenir des conseils\n2. J'ai besoin d'une assistance urgente\n3. Soumettre des commentaires\n4. Conseils de santé",
        'violence_menu': "Si vous avez subi des violences, appelez:\n Kubuntu (Gratuit): <b>3029<b> \n Ou les numéros réguliers: <b>0788267884/ \n 0782797015 <b>\n Vous pouvez également envoyer un email à: <b>francoiseuwamriya050@gmail.com<b>",
        'health_tips': "Conseils de santé:\n1. Mangez équilibré\n2. Faites de l'exercice pendant vos règles\n3. Prenez soin de votre santé mentale\n4. Retour",
        'feedback': "Merci pour vos commentaires. Nous les utilisons pour améliorer le système."
    }
}

def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")
    language = 'rw'  # Default language (can be dynamically set)

    response = ""

    # Language selection
    if text == "":
        response = "CON Choose your language:\n1. Kinyarwanda\n2. English\n3. Français"
    elif text == "1":
        language = 'rw'
        response = f"CON {LANGUAGES[language]['welcome']}"
    elif text == "2":
        language = 'en'
        response = f"CON {LANGUAGES[language]['welcome']}"
    elif text == "3":
        language = 'fr'
        response = f"CON {LANGUAGES[language]['welcome']}"

    # Registration
    elif text == "7":
        response = "CON Andika izina ryawe:"
    elif text.startswith("7*"):
        details = text.split("*")
        if len(details) == 2:
            response = "CON Andika nimero yawe ya telefono:"
        elif len(details) == 3:
            response = "CON Andika ijambo ry'ibanga:"
        elif len(details) == 4:
            register_user(details[1], details[2], details[3])
            response = "END Murakoze kwiyandikisha. Mwongere mugerageze."

    elif text.startswith("1"):
        if text == "1":
            response = f"CON {LANGUAGES[language]['parent_menu']}"
        elif text == "1*1":
            response = f"CON {LANGUAGES[language]['parent_main_menu']}"
        elif text.startswith("1*1*1"):
            response = "CON Andika amazina yawe yose:"
    elif text.startswith("1*1*2*"):
        parts = text.split("*")
        if len(parts) == 4:
            names = parts[-1]  # Extract the names from the user input
            response = "CON Andika ijambo ryibanga rishya:"
        elif len(parts) == 5:
            password = parts[-1]  # Extract the new password from the user input
            # Here you can add the logic to save the user's names and password and proceed with the registration process
            register_user(phone_number, names, password)  # Save the user's profile to the database
            response = "END Murakoze kwiyandikisha. Konti yanyu yashyizweho neza."

        elif text.startswith("1*1*2*"):
            password = text.split("*")[-1]  # Extract the password from the user input
            user = get_user_profile(phone_number)  # Fetch the user's profile from the database

            if user and check_password_hash(user.password_hash, password):  # Check if the password matches
                response = f"CON {LANGUAGES[language]['parent_menu']}"  # Return to the parent menu
            else:
                response = (
                    "END Ijambo ryibanga ntabwo ari ryo. Hitamo:\n"
                    "1. Kanda kwiyandikisha niba utarafite konti.\n"
                    "2. Hindura ijambo ryibanga niba waribagiwe."
                )

            response = "CON Andika uburebure bw'ukwezi (mu minsi, urugero: 28):"
        elif text.startswith("1*1*"):
            details = text.split("*")
            if len(details) == 3:
                try:
                    cycle_length = int(details[2])
                    response = "CON Andika itariki ya mbere y'igihe cy'ukwezi (DD/MM/YYYY):"
                except ValueError:
                    response = "CON Umubare wanditse si wo. Andika umubare w'iminsi (urugero: 28):"
            elif len(details) == 4:
                try:
                    last_period_date = details[3]
                    next_period, ovulation, fertile_start, fertile_end = calculate_cycle_dates(last_period_date, int(details[2]))
                    response = (
                        f"END Igihe cy'ukwezi gikurikira ni {next_period.strftime('%d/%m/%Y')}.\n"
                        f"Igihe cyo gusama: {ovulation.strftime('%d/%m/%Y')}.\n"
                        f"Iminsi y'uburumbuke: {fertile_start.strftime('%d/%m/%Y')} kugeza {fertile_end.strftime('%d/%m/%Y')}."
                    )
                except ValueError:
                    response = "CON Itariki wanditse si yo. Andika mu buryo bwa DD/MM/YYYY:"
        elif text == "1*2":
            children = get_children(phone_number)
            if children:
                response = "END Abana mwiyandikishije:\n"
                for child in children:
                    next_period, ovulation, _, _ = calculate_cycle_dates(child[4], child[3])
                    response += (
                        f"{child[2]} - Igihe cy'ukwezi gikurikira: {next_period.strftime('%d/%m/%Y')}, "
                        f"Igihe cyo gusama: {ovulation.strftime('%d/%m/%Y')}\n"
                    )
            else:
                response = "END Nta mwana mwiyandikishije. Hitamo 3 kugira ngo mwiyandikishe umwana."
        elif text == "1*3":
            response = "CON Andika izina ry'umwana wawe:"
        elif text.startswith("1*3*"):
            details = text.split("*")
            if len(details) == 3:
                response = "CON Andika uburebure bw'ukwezi (mu minsi, urugero: 28):"
            elif len(details) == 4:
                try:
                    cycle_length = int(details[3])
                    response = "CON Andika itariki ya mbere y'igihe cy'ukwezi (DD/MM/YYYY):"
                except ValueError:
                    response = "CON Umubare wanditse si wo. Andika umubare w'iminsi (urugero: 28):"
            elif len(details) == 5:
                try:
                    last_period_date = details[4]
                    datetime.strptime(last_period_date, "%d/%m/%Y")
                    save_child(phone_number, details[2], int(details[3]), last_period_date)
                    response = "END Umwana wawe yiyandikishije neza! Murakoze."
                except ValueError:
                    response = "CON Itariki wanditse si yo. Andika mu buryo bwa DD/MM/YYYY:"
        elif text == "1*4":
            response = "CON Andika izina rishya ryo kuvugurura konti:"
        elif text.startswith("1*4*"):
            details = text.split("*")
            if len(details) == 3:
                update_account(phone_number, details[2])
                response = "END Konti yavuguruwe neza."
        elif text == "1*5":
            delete_account(phone_number)
            response = "END Konti yasibwe neza."
        elif text == "1*6":
            response = "CON Andika izina ry'umwana ushaka gusiba:"
        elif text.startswith("1*6*"):
            details = text.split("*")
            if len(details) == 3:
                delete_child(phone_number, details[2])
                response = "END Umwana yasibwe neza muri sisitemu."
        elif text == "1*7":
            response = "CON Andika ibitekerezo byawe:"
        elif text.startswith("1*7*"):
            feedback = text.split("*", 1)[1]
            submit_feedback(phone_number, feedback)
            response = f"END {LANGUAGES[language]['feedback']}"
        elif text == "1*8":
            response = f"CON {LANGUAGES[language]['health_tips']}"
        elif text.startswith("1*8*"):
            tip_id = text.split("*")[2]
            tip = get_health_tips(tip_id)
            response = f"END {tip}"

    # Teen menu
    elif text.startswith("2"):
        if text == "2":
            response = f"CON {LANGUAGES[language]['teen_menu']}"
        elif text == "2*1":
            response = "CON Andika uburebure bw'ukwezi (mu minsi, urugero: 28):"
        elif text.startswith("2*1*"):
            details = text.split("*")
            if len(details) == 3:
                try:
                    cycle_length = int(details[2])
                    response = "CON Andika itariki ya mbere y'igihe cy'ukwezi (DD/MM/YYYY):"
                except ValueError:
                    response = "CON Umubare wanditse si wo. Andika umubare w'iminsi (urugero: 28):"
            elif len(details) == 4:
                try:
                    last_period_date = details[3]
                    next_period, ovulation, fertile_start, fertile_end = calculate_cycle_dates(last_period_date, int(details[2]))
                    response = (
                        f"END Igihe cy'ukwezi gikurikira ni {next_period.strftime('%d/%m/%Y')}.\n"
                        f"Igihe cyo gusama: {ovulation.strftime('%d/%m/%Y')}.\n"
                        f"Iminsi y'uburumbuke: {fertile_start.strftime('%d/%m/%Y')} kugeza {fertile_end.strftime('%d/%m/%Y')}."
                    )
                except ValueError:
                    response = "CON Itariki wanditse si yo. Andika mu buryo bwa DD/MM/YYYY:"
        elif text == "2*2":
            response = "CON Andika ijambo rifitanye isano n'amakuru ushaka kuri gahunda y'ubuzima (urugero: Imirire):"
        elif text.startswith("2*2*"):
            details = text.split("*")
            if len(details) == 3:
                guidance = fetch_nutrition_guidance(details[2])
                response = f"END Murakoze! Amakuru ajyanye n'{details[2]} :\n{guidance}"
            else:
                response = "END Hari ikibazo mu kwinjiza amakuru yawe."
        elif text == "2*3":
            response = "CON Andika ibitekerezo byawe:"
        elif text.startswith("2*3*"):
            feedback = text.split("*", 1)[1]
            submit_feedback(phone_number, feedback)
            response = f"END {LANGUAGES[language]['feedback']}"
        elif text == "2*4":
            response = f"CON {LANGUAGES[language]['health_tips']}"
        elif text.startswith("2*4*"):
            tip_id = text.split("*")[2]
            tip = get_health_tips(tip_id)
            response = f"END {tip}"

    # Pregnant menu
    elif text.startswith("3"):
        if text == "3":
            response = f"CON {LANGUAGES[language]['pregnant_menu']}"
        elif text == "3*1":
            response = "CON Andika ibyo wariye uyu munsi:"
        elif text.startswith("3*1*"):
            meal = text.split("*", 2)[-1]
            save_meal(phone_number, meal)
            meal_history = get_meal_history(phone_number)
            guidance = get_nutrition_guidance(meal_history)
            response = f"END Based on your recent meals, we recommend: {guidance}"
        elif text == "3*2":
            response = "CON Andika ibitekerezo byawe:"
        elif text.startswith("3*2*"):
            feedback = text.split("*", 1)[1]
            submit_feedback(phone_number, feedback)
            response = f"END {LANGUAGES[language]['feedback']}"
        elif text == "3*3":
            response = f"CON {LANGUAGES[language]['health_tips']}"
        elif text.startswith("3*3*"):
            tip_id = text.split("*")[2]
            tip = get_health_tips(tip_id)
            response = f"END {tip}"

    # Doctor menu
    elif text.startswith("4"):
        if text == "4":
            response = f"CON {LANGUAGES[language]['doctor_menu']}"
        elif text == "4*1":
            response = "CON Andika ikibazo cyawe cyo kuvugana na muganga:"
        elif text.startswith("4*1*"):
            issue = text.split("*", 1)[1]
            schedule_appointment(phone_number, issue)
            response = "END Twakiriye ikibazo cyawe. Muganga azakubwira vuba."
        elif text == "4*2":
            contacts = get_emergency_contacts()
            response = f"END Nimero z'ubufasha bwihutirwa:\n{contacts}"
        elif text == "4*3":
            response = "CON Andika ibitekerezo byawe:"
        elif text.startswith("4*3*"):
            feedback = text.split("*", 1)[1]
            submit_feedback(phone_number, feedback)
            response = f"END {LANGUAGES[language]['feedback']}"
        elif text == "4*4":
            response = f"CON {LANGUAGES[language]['health_tips']}"
        elif text.startswith("4*4*"):
            tip_id = text.split("*")[2]
            tip = get_health_tips(tip_id)
            response = f"END {tip}"

    # Violence support menu
    elif text.startswith("5"):
        if text == "5":
            response = f"CON {LANGUAGES[language]['violence_menu']}"
        elif text == "5*1":
            send_sms(phone_number, "Ubufasha bwihutirwa bwatumijwe. Mwihangane.")
            response = "END Twakoherereje ubutumwa. Mwihangane."

    # Health tips menu
    elif text.startswith("6"):
        if text == "6":
            response = f"CON {LANGUAGES[language]['health_tips']}"
        elif text.startswith("6*"):
            tip_id = text.split("*")[1]
            if tip_id == "4":
                response = f"CON {LANGUAGES[language]['welcome']}"
            else:
                tip = get_health_tips(tip_id)
                response = f"END {tip}"

    # Invalid option
    else:
        response = f"END {LANGUAGES[language].get('invalid_option', 'Invalid option. Please try again.')}"

    return response, 200, {"Content-Type": "text/plain"}