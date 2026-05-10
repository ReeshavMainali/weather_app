RAINY = {51, 53, 55, 61, 63, 65, 80, 81, 82}
STORMY = {82, 95, 96, 99}
SNOWY  = {71, 73, 75, 77, 85, 86}
FOGGY  = {45, 48}

def get_advice(code: int, temp: float, wind: float, humidity: int, uv: int) -> list[dict]:
    tags = []

    is_rainy  = code in RAINY
    is_stormy = code in STORMY
    is_snowy  = code in SNOWY
    is_foggy  = code in FOGGY
    is_clear  = code in {0, 1}
    is_cloudy = code == 3
    is_warm   = temp >= 25
    is_hot    = temp >= 30 
    is_cold   = temp <= 5
    is_windy  = wind >= 30

    def tag(text, kind):
        tags.append({"text": text, "kind": kind})
    
    if is_stormy:                        
        tag("Stay indoors", "bad")
    if is_rainy:                         
        tag("Bring an umbrella", "warn")
    if is_snowy:                         
        tag("Bundle up for snow", "warn")
    if is_foggy:                         
        tag("Drive carefully", "warn")
    if is_windy:                         
        tag("Strong winds — hold on", "warn")
    if is_hot:                           
        tag("Stay hydrated", "warn")
    if is_cold:                          
        tag("Wear a heavy coat", "warn")
    if uv >= 6:                          
        tag(f"Apply sunscreen (UV {uv})", "warn")
    if humidity > 80 and not is_rainy and is_warm:   
        tag("Feels muggy outside", "warn")

    if is_clear and is_warm and not is_windy:
        tag("Great day for a hike", "good")
    if is_clear and not is_hot:
        tag("Perfect for drying laundry", "good")
    if is_clear and is_warm and not is_windy:
        tag("Nice day for a picnic", "good")
    if is_clear and not is_hot and not is_cold and not is_windy and humidity <= 80:
        tag("Open your windows", "good")
    if not is_rainy and not is_stormy and not is_windy and not is_cold and not is_foggy:
        tag("Good for cycling", "good")
    if is_rainy and not is_stormy:
        tag("Good reading weather", "good")
    if is_cloudy and not is_rainy:
        tag("Decent for a walk", "good")
    if is_rainy and not is_stormy:
        tag("Skip outdoor plans", "bad")

    if not tags:
        tag("Fairly ordinary day", "good")

    return tags