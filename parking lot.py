RATE = 2


class Car:
    def __init__(self, plate, spot):
        self.plate = plate
        self.spot = spot

    def calculate_fee(self, hours):
        if hours <= 0:
            return None
        return hours * RATE


class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cars = {}
        self.earnings = 0

    def find_free_spot(self):
        used_spots = []
        for car in self.cars.values():
            used_spots.append(car.spot)
        for spot in range(1, self.capacity + 1):
            if spot not in used_spots:
                return spot
        return None

    def park_car(self, plate):
        plate = plate.strip().upper()
        if plate == "":
            return "Plate number cannot be empty."
        if "," in plate:
            return "Plate number cannot contain a comma."
        if plate in self.cars:
            return "This car is already parked."
        spot = self.find_free_spot()
        if spot is None:
            return "Parking lot is full."
        self.cars[plate] = Car(plate, spot)
        return "Car parked in spot " + str(spot) + "."

    def remove_car(self, plate, hours):
        plate = plate.strip().upper()
        if plate not in self.cars:
            return "Car not found."
        fee = self.cars[plate].calculate_fee(hours)
        if fee is None:
            return "Hours must be greater than zero."
        spot = self.cars[plate].spot
        del self.cars[plate]
        self.earnings += fee
        return "Car removed from spot " + str(spot) + ". Fee: $" + str(fee)

    def view_spots(self):
        result = []
        for spot in range(1, self.capacity + 1):
            label = "Available"
            for car in self.cars.values():
                if car.spot == spot:
                    label = car.plate
            result.append((spot, label))
        return result

    def statistics(self):
        occupied = len(self.cars)
        free = self.capacity - occupied
        percent = occupied * 100 / self.capacity
        return occupied, free, percent, self.earnings

    def save_data(self):
        try:
            file = open("parking_data.txt", "w")
            file.write(str(self.capacity) + "," + str(self.earnings) + "\n")
            for car in self.cars.values():
                file.write(car.plate + "," + str(car.spot) + "\n")
            file.close()
            return "Data saved successfully."
        except OSError:
            return "Could not save data."

    def load_data(self):
        try:
            file = open("parking_data.txt", "r")
            lines = file.readlines()
            file.close()
        except FileNotFoundError:
            return "No saved file found."
        except OSError:
            return "Could not read the saved file."


        try:
            first = lines[0].strip().split(",")
            if len(first) != 2:
                return "Saved file contains invalid data."
            capacity = int(first[0])
            earnings = float(first[1])
            if capacity <= 0 or earnings < 0:
                return "Saved file contains invalid data."

            new_cars = {}
            used_spots = []
            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) != 2:
                    return "Saved file contains invalid data."
                plate = parts[0]
                spot = int(parts[1])
                if plate == "" or plate != plate.strip().upper():
                    return "Saved file contains invalid data."
                if spot < 1 or spot > capacity:
                    return "Saved file contains invalid data."
                if plate in new_cars or spot in used_spots:
                    return "Saved file contains invalid data."
                new_cars[plate] = Car(plate, spot)
                used_spots.append(spot)
        except (ValueError, IndexError, OverflowError):
            return "Saved file contains invalid data."

        if len(new_cars) > capacity:
            return "Saved file contains invalid data."
        self.capacity = capacity
        self.earnings = earnings
        self.cars = new_cars
        return "Data loaded successfully."


def read_positive_number(prompt):
    while True:
        value = input(prompt)
        try:
            number = int(value)
            if number > 0:
                return number
        except ValueError:
            pass
        print("Please enter a positive whole number.")


def main():
    lot = ParkingLot(10)

    lot.park_car("ABC123")
    lot.park_car("XYZ789")

    while True:
        print("\n===== PARKING LOT MANAGER =====")
        print("1. Park a Car")
        print("2. Remove a Car")
        print("3. View Parking Lot")
        print("4. Parking Statistics")
        print("5. Save Data")
        print("6. Load Data")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            plate = input("Enter plate number: ")
            print(lot.park_car(plate))
        elif choice == "2":
            plate = input("Enter plate number: ").strip().upper()
            if plate not in lot.cars:
                print("Car not found.")
            else:
                hours = read_positive_number("Enter parked hours: ")
                print(lot.remove_car(plate, hours))
        elif choice == "3":
            for spot, label in lot.view_spots():
                print("Spot", spot, "-", label)
        elif choice == "4":
            occupied, free, percent, earnings = lot.statistics()
            print("Occupied spots:", occupied)
            print("Free spots:", free)
            print("Occupancy: " + str(round(percent, 1)) + "%")
            print("Total earnings: $" + str(earnings))
        elif choice == "5":
            print(lot.save_data())
        elif choice == "6":
            print(lot.load_data())
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1 to 7.")


if __name__ == "__main__":
    main()
