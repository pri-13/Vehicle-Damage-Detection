# estimate approximate vehicle damage location

class LocationEstimator:

    def estimate(
        self,
        damage_type,
        bbox,
        image_width,
        image_height
    ):

        x1, y1, x2, y2 = bbox
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # horizontal
        if cx < image_width / 3:
            horizontal = "Left"
        elif cx < 2 * image_width / 3:
            horizontal = "Center"
        else:
            horizontal = "Right"

        # vertical
        if cy < image_height / 3:
            vertical = "Front"
        elif cy < 2 * image_height / 3:
            vertical = "Middle"
        else:
            vertical = "Rear"

        damage_type = damage_type.lower()

        # lamp
        if damage_type == "lamp broken":
            if vertical == "Front":
                return f"Front {horizontal} Lamp"
            return f"Rear {horizontal} Lamp"
        # glass
        if damage_type == "glass shatter":
            if vertical == "Front":
                return "Front Windshield"
            return "Rear Windshield"
        #tire
        if damage_type == "tire flat":
            if vertical == "Front":
                return f"Front {horizontal} Tire"
            return f"Rear {horizontal} Tire"
        # general body parts
        mapping = {
            ("Front", "Left"):
                "Front Left Panel",
            ("Front", "Center"):
                "Front Bumper",
            ("Front", "Right"):
                "Front Right Panel",
            ("Middle", "Left"):
                "Left Door",
            ("Middle", "Center"):
                "Center Body",
            ("Middle", "Right"):
                "Right Door",
            ("Rear", "Left"):
                "Rear Left Panel",
            ("Rear", "Center"):
                "Rear Bumper",
            ("Rear", "Right"):
                "Rear Right Panel"
        }
        return mapping[(vertical, horizontal)]