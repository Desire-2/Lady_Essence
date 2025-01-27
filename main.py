from flask import Flask, request
from database import init_db, save_parent, save_child, get_children, update_account, delete_account, delete_child
from guidance import save_planetary_guidance, fetch_nutrition_guidance
from helpers import calculate_cycle_dates
from datetime import datetime

app = Flask(__name__)

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    response = ""

    if text == "":
        response = "CON Murakaza neza muri Sisitemu (<b>Lady’s Essence</b>)\n"
        response += "1. Ndi Umubyeyi\n"
        response += "2. Ndi Umwangavu/Ushakashaka\n"
    elif text == "1":
        response = "CON Murakaza neza ku rubuga rw'ababyeyi:\n"
        response += "1. Gukurikirana igihe cy'ukwezi kwanjye\n"
        response += "2. Gukurikirana igihe cy'ukwezi cy'abana banjye\n"
        response += "3. Kwiyandikisha umwana\n"
        response += "4. Kuvugurura konti yanjye\n"
        response += "5. Gusiba konti\n"
        response += "6. Gusiba umwana\n"
    elif text == "1*1":
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
                datetime.strptime(last_period_date, "%d/%m/%Y")
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
    elif text == "2":
        response = "CON Murakaza neza ku rubuga rw'abangavu/ushakashaka:\n"
        response += "1. Gukurikirana igihe cy'ukwezi kwanjye\n"
        response += "2. Kugisha inama ku mirire n'ubuzima\n"
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
                datetime.strptime(last_period_date, "%d/%m/%Y")
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
            save_planetary_guidance(phone_number, guidance)
            response = f"END Murakoze! Amakuru ajyanye n'{details[2]} :\n{guidance}"
        else:
            response = "END Hari ikibazo mu kwinjiza amakuru yawe."
    else:
        response = "END Amahitamo si yo. Gerageza ubundi."

    return response, 200, {"Content-Type": "text/plain"}

if __name__ == '__main__':
    init_db()
    app.run(port=5000)
