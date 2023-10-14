import threading
import time
import datetime

# current local time
datetime_object = str(datetime.datetime.now())
current_hr = int(datetime_object[11:13])
current_min = int(datetime_object[14:16])
current_time = str(current_hr) + ":" + str(current_min)

# current status print format creation
spacer = "--------------------------------------------"
current_status = []

# initialization
for i in range(5):
    num = str(i + 1)
    this = ['machine_' + num, 'empty', 'No user', '00:00', '0 min left']
    current_status.append(this)

# current status list creation
def current_status_print():
    result = ""
    for i in range(len(current_status)):
        result += f"{current_status[i]} \n"
    print(spacer, "Current Time is " + current_time, "Current Status: ", result, spacer, sep="\n")


# information of each laundry status for current status list
class Info:
    def set_machinename(self, machinename):
        self.machinename = machinename

    def set_availability(self, availability):
        self.availability = availability

    def set_user(self, user):
        self.user = user

    def set_endingtime(self, endingtime):
        self.endingtime = endingtime

    def set_remainingtime(self, remainingtime):
        self.remainingtime = remainingtime

    def set_info_list(self, machine_selection):
        self.info_list = [self.machinename, self.availability, self.user, self.endingtime, self.remainingtime]
        current_status[machine_selection - 1] = self.info_list


# available machines list
def available_machines():
    available_machines = []
    for i in range(len(current_status)):
        if current_status[i][1] != "running":
            available_machines.append(current_status[i][0])
    print(available_machines, end="")


def laundry_start():
    machine_name = ""
    current_status_print()
    available_machines()
    print(" are currently available.")

    while True:

        while True:
            try:
                machine_selection = int((input("Which machine are you going to use? Machine number = ")))
                break
            except ValueError:
                print("Please enter a number.")

        if machine_selection not in range(1, len(current_status) + 1):
            print("The machine you entered does not exist.")
            continue
        elif current_status[machine_selection - 1][1] != "empty":
            print("The machine is currently used by someone else. Please select another machine.")
            continue
        elif current_status[machine_selection - 1][1] == "empty":

            locals()['machine_%d' % machine_selection] = Info()
            locals()['machine_%d' % machine_selection].set_availability("running")
            user = input("selected machine: " + str(machine_selection) + "\n  enter your name: ")
            locals()['machine_%d' % machine_selection].set_machinename('machine_%d' % machine_selection)
            locals()['machine_%d' % machine_selection].set_user(user)

            # setting user & current time info
            print("username: " + user)

            while True:
                try:
                    running_time = int(input("enter your running time for this machine: (min)"))
                    break
                except ValueError:
                    print("Please reenter a number")

            min = running_time
            all_set_alert = f"Machine{machine_selection} All set! We'll send you notice when it is almost done."
            print(all_set_alert)
            print("Current time is " + current_time)

            # estimating the ending time
            est_hr = current_hr
            est_min = current_min
            if running_time >= 60:
                est_hr += running_time // 60
                est_min += running_time % 60

            else:
                est_min += running_time

            if est_min >= 60:
                est_hr += 1
                est_min = abs(est_min - 60)
            if est_hr >= 24:
                est_hr = est_hr - 24

            est_end = str(est_hr) + ":" + str(est_min)
            locals()['machine_%d' % machine_selection].set_endingtime(est_end)
            locals()['machine_%d' % machine_selection].set_remainingtime("%d min left" % min)
            locals()['machine_%d' % machine_selection].set_info_list(machine_selection)
            print(f"machine_" + str(machine_selection) + " laundry will be finished at " + est_end)
            threading.Thread(target=laundry_start).start()

            # remaining time until the laundry ends
            while min != 0:
                five_minute_alert = "\n" + "Machine_" + str(machine_selection) + " is 5 minutes left to be finished"
                end_alert = "\n" + "Machine_" + str(machine_selection) + " laundry is finished. Recollect your items"

                if min == 5:
                    print(five_minute_alert)
                min = min - 1
                locals()['machine_%d' % machine_selection].set_remainingtime("%d min left" % min)
                locals()['machine_%d' % machine_selection].set_info_list(machine_selection)

                time.sleep(1)
                # Originally, time.sleep(60) should be used to calculate minutes.
                # time.sleep(1) is used here for the convenience of testing the program

            else:
                pass
            print(end_alert)
            locals()['machine_%d' % machine_selection].set_availability("empty")
            locals()['machine_%d' % machine_selection].set_user("No user")
            locals()['machine_%d' % machine_selection].set_endingtime("00:00")
            locals()['machine_%d' % machine_selection].set_remainingtime("0 min left")
            locals()['machine_%d' % machine_selection].set_info_list(machine_selection)
            current_status_print()

            break


threading.Thread(target=laundry_start).start()