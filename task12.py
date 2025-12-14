import csv
import json
import os
from datetime import datetime

PATIENT_CSV = "patients.csv"
BACKUP_JSON = "backup.json"
AUDIT_LOG = "audit.log"

# DATA STRUCTURES
# patients: { patient_id: { "name": __, "diagnosis": ___, "medications":[ ] }
patients = {}

# appointments: list of tuples (date, time, doctor, patient_id)
appointments = []

# HELPER: AUDIT LOGGING
def log_action(action_label, details=""):
    """
    Append an action line to audit.log.
    Format:
    TIMESTAMP - <human text> | ACTION_CODE | extra details...

    Example human text:
    "Appointment canceled for ID 101"
    """
    timestamp = datetime.now().isoformat(timespec="seconds")
    human_text = details if details else action_label
    line = f"{timestamp} - {human_text} | {action_label}\n"
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def log_appointment_action(action_code, date, time, doctor, patient_id, human_text):
    """
    More structured log line for actions we want to ROLLBACK later.

    Format:
    TIMESTAMP - human text | ACTION_CODE | date | time | doctor | patient_id
    """
    timestamp = datetime.now().isoformat(timespec="seconds")
    line = (
        f"{timestamp} - {human_text} | {action_code} | "
        f"{date} | {time} | {doctor} | {patient_id}\n"
    )
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(line)


# LOAD PATIENTS FROM CSV
def load_patients_from_csv(filename=PATIENT_CSV):
    """
    CSV format expected:
    id,name,diagnosis,medications

    medications field can be like: "paracetamol;ibuprofen"
    """
    global patients
    if not os.path.exists(filename):
        print(f"[INFO] {filename} not found. Starting with empty patient list.")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pid = row.get("id", "").strip()
                if not pid:
                    continue
                name = row.get("name", "").strip()
                diagnosis = row.get("diagnosis", "").strip()
                meds_raw = row.get("medications", "").strip()
                medications = [m.strip() for m in meds_raw.split(";")] if meds_raw else []
                patients[pid] = {
                    "name": name,
                    "diagnosis": diagnosis,
                    "medications": medications,
                }
        print("[OK] Patients loaded from CSV.")
        log_action("LOAD_PATIENTS", f"Patients loaded from {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to load patients: {e}")
        log_action("LOAD_PATIENTS_ERROR", f"Failed to load {filename}: {e}")


# APPOINTMENT VALIDATION
def has_appointment_conflict(date, time, doctor, patient_id):
    """
    Check if there is an overlapping appointment.
    Simple rule:
    - Same date+time with same doctor OR same patient is not allowed.
    """
    for (d, t, doc, pid) in appointments:
        if d == date and t == time:
            if doc == doctor:
                print("[CONFLICT] Doctor already has an appointment at this time.")
                return True
            if pid == patient_id:
                print("[CONFLICT] Patient already has an appointment at this time.")
                return True
    return False


# SCHEDULE / CANCEL APPOINTMENT
def schedule_appointment():
    date = input("Enter appointment date (YYYY-MM-DD): ").strip()
    time = input("Enter appointment time (HH:MM): ").strip()
    doctor = input("Enter doctor name: ").strip()
    patient_id = input("Enter patient ID: ").strip()

    if patient_id not in patients:
        print("[ERROR] Patient ID not found.")
        log_action("SCHEDULE_FAIL", f"Invalid patient ID {patient_id}")
        return

    if has_appointment_conflict(date, time, doctor, patient_id):
        log_action(
            "SCHEDULE_CONFLICT",
            f"Conflict trying to schedule {patient_id} with {doctor} on {date} {time}",
        )
        return

    # Add appointment as tuple
    appt = (date, time, doctor, patient_id)
    appointments.append(appt)
    print("[OK] Appointment scheduled successfully.")
    log_appointment_action(
        "ADD_APPOINTMENT",
        date,
        time,
        doctor,
        patient_id,
        f"Appointment scheduled for ID {patient_id}",
    )


def cancel_appointment():
    date = input("Enter appointment date to cancel (YYYY-MM-DD): ").strip()
    time = input("Enter appointment time to cancel (HH:MM): ").strip()
    doctor = input("Enter doctor name: ").strip()
    patient_id = input("Enter patient ID: ").strip()

    # Find the appointment
    index_to_remove = None
    for i, (d, t, doc, pid) in enumerate(appointments):
        if d == date and t == time and doc == doctor and pid == patient_id:
            index_to_remove = i
            break

    if index_to_remove is None:
        print("[ERROR] No matching appointment found.")
        log_action(
            "CANCEL_FAIL",
            f"Cancel failed; no appointment for {patient_id} with {doctor} on {date} {time}",
        )
        return

    # Before removing, we log enough info so rollback can re-create it
    appointments.pop(index_to_remove)
    print("[OK] Appointment canceled.")
    log_appointment_action(
        "CANCEL_APPOINTMENT",
        date,
        time,
        doctor,
        patient_id,
        f"Appointment canceled for ID {patient_id}",
    )


def show_appointments():
    if not appointments:
        print("No appointments scheduled.")
        return
    print("\n--- Appointments ---")
    for (date, time, doctor, patient_id) in appointments:
        p = patients.get(patient_id, {})
        name = p.get("name", "Unknown")
        print(f"{date} {time} - {doctor} with {name} (ID: {patient_id})")
    print("-----")


# TREATMENT REPORT
def generate_treatment_report():
    """
    Group patients by diagnosis and print report.
    """
    if not patients:
        print("[INFO] No patient data to report.")
        return

    diagnosis_groups = {}
    for pid, pdata in patients.items():
        diag = pdata.get("diagnosis", "Unknown")
        diagnosis_groups.setdefault(diag, []).append((pid, pdata))

    print("\n=== Treatment Report (Grouped by Diagnosis) ===")
    for diag, plist in diagnosis_groups.items():
        print(f"\nDiagnosis: {diag}")
        print("-" * (len("Diagnosis: ") + len(diag)))
        for pid, pdata in plist:
            meds = ", ".join(pdata.get("medications", [])) or "None"
            print(f"  ID: {pid}, Name: {pdata['name']}, Medications: {meds}")
    print("===========")

    log_action("TREATMENT_REPORT", "Generated treatment report by diagnosis")


# BACKUP / RESTORE JSON
def backup_to_json(filename=BACKUP_JSON):
    """
    Backup patients and appointments to JSON.
    """
    data = {
        "patients": patients,
        "appointments": [list(a) for a in appointments],  # tuples -> lists for JSON
    }
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("[OK] Backup saved to JSON.")
        log_action("BACKUP_OK", f"Backup saved to {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to backup: {e}")
        log_action("BACKUP_ERROR", f"Backup failed: {e}")


def restore_from_json(filename=BACKUP_JSON):
    """
    Restore data from backup JSON.
    Handle corrupted file or bad format with try/except.
    """
    global patients, appointments
    if not os.path.exists(filename):
        print(f"[WARN] Backup file {filename} not found.")
        log_action("RESTORE_MISSING", f"{filename} not found")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate structure
        if "patients" not in data or "appointments" not in data:
            raise ValueError("Invalid backup structure")

        patients = data["patients"]
        # Convert lists back to tuples
        appointments = [tuple(a) for a in data["appointments"]]
        print("[OK] Data restored from backup.")
        log_action("RESTORE_OK", f"Data restored from {filename}")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[ERROR] Backup file is corrupted or invalid: {e}")
        log_action("RESTORE_CORRUPT", f"Corrupted backup: {e}")
        # Recovery strategy: keep current in-memory data, don't crash
    except Exception as e:
        print(f"[ERROR] Unknown error restoring backup: {e}")
        log_action("RESTORE_ERROR", f"Restore failed: {e}")


# HARD CHALLENGE: ROLLBACK
def rollback_last_actions(n=3):
    """
    Undo last n appointment actions (ADD_APPOINTMENT / CANCEL_APPOINTMENT)
    by reading audit.log from the bottom.

    Logic:
    - For last N lines that contain these codes:
      * ADD_APPOINTMENT -> remove that appointment if it exists
      * CANCEL_APPOINTMENT -> re-add that appointment if it does not exist
    """
    global appointments

    if not os.path.exists(AUDIT_LOG):
        print("[WARN] No audit.log file found. Nothing to rollback.")
        return

    try:
        with open(AUDIT_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[ERROR] Cannot read audit.log: {e}")
        return

    if not lines:
        print("[INFO] audit.log is empty. Nothing to rollback.")
        return

    actions_undone = 0

    # Read from the end (most recent actions first)
    for line in reversed(lines):
        if actions_undone >= n:
            break

        parts = [p.strip() for p in line.strip().split("|")]

        # Looking for lines with structure:
        # TIMESTAMP - human text | ACTION_CODE | date | time | doctor | patient_id
        if len(parts) < 6:
            continue  # not a structured appointment log

        action_code = parts[1]
        if action_code not in ("ADD_APPOINTMENT", "CANCEL_APPOINTMENT"):
            continue

        date = parts[2]
        time = parts[3]
        doctor = parts[4]
        patient_id = parts[5]

        appt = (date, time, doctor, patient_id)

        if action_code == "ADD_APPOINTMENT":
            # To rollback ADD, we REMOVE the appointment
            if appt in appointments:
                appointments.remove(appt)
                actions_undone += 1
                print(f"[ROLLBACK] Removed appointment {appt}")
        elif action_code == "CANCEL_APPOINTMENT":
            # To rollback CANCEL, we RE-ADD the appointment
            if appt not in appointments:
                # Also respect conflict rules? For rollback we generally
                # ignore conflicts and force it back.
                appointments.append(appt)
                actions_undone += 1
                print(f"[ROLLBACK] Re-added appointment {appt}")

    if actions_undone == 0:
        print("[INFO] No appointment actions found to rollback.")
    else:
        print(f"[OK] Rollback complete. {actions_undone} actions undone.")
        log_action("ROLLBACK_DONE", f"Rolled back {actions_undone} actions")


# MENU / MAIN LOOP
def show_patients():
    if not patients:
        print("No patients loaded.")
        return
    print("\n--- Patients ---")
    for pid, pdata in patients.items():
        meds = ", ".join(pdata.get("medications", [])) or "None"
        print(
            f"ID: {pid}, Name: {pdata['name']}, "
            f"Diagnosis: {pdata['diagnosis']}, Medications: {meds}"
        )
    print("-----")


def main_menu():
    load_patients_from_csv()

    while True:
        print("\n=== Hospital Patient Management System ===")
        print("1. Show all patients")
        print("2. Schedule appointment")
        print("3. Cancel appointment")
        print("4. Show appointments")
        print("5. Generate treatment report")
        print("6. Backup to JSON")
        print("7. Restore from backup")
        print("8. Rollback last 3 actions")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_patients()
        elif choice == "2":
            schedule_appointment()
        elif choice == "3":
            cancel_appointment()
        elif choice == "4":
            show_appointments()
        elif choice == "5":
            generate_treatment_report()
        elif choice == "6":
            backup_to_json()
        elif choice == "7":
            restore_from_json()
        elif choice == "8":
            rollback_last_actions(3)
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
