"""
Example script demonstrating jyotishyamitra library usage.
This script generates a complete Vedic astrology chart for Swami Vivekananda
using Lahiri ayanamsa (sidereal calculations).

Birth Details:
- Name: Swami Vivekananda  
- Date: 12 January 1863
- Time: 6:33 AM
- Place: Kolkata, India (22.53°N, 88.36°E, GMT+5:53)
"""

import jyotishyamitra as jsm

print("=== Jyotishyamitra Example - Swami Vivekananda's Chart ===")
print("Generating complete Vedic astrology chart using Lahiri ayanamsa...")
print()

#For input related functions
jsm.clear_birthdata()

################ Providing input birth data ####################
# Using Swami Vivekananda's birth details (12 January 1863, 6:33 AM, Kolkata)
#providing Name and Gender
inputdata = jsm.input_birthdata(name="Vivekananda, Swami", gender="male")

#providing Date of birth details
inputdata = jsm.input_birthdata(year="1863", month="1", day="12")

#Providing Place of birth details (Kolkata, India)
inputdata = jsm.input_birthdata(place="Kolkata, India", longitude="+88.36", lattitude="+22.53", timezone="+5.88")

#Providing Time of birth details (6:33 AM)
inputdata = jsm.input_birthdata(hour="6", min="33", sec="0")

################### Lets Validate Birthdata ######################
jsm.validate_birthdata()

#If Birthdata is valid then get birthdata
if(jsm.IsBirthdataValid()):
    birthdata = jsm.get_birthdata()


########### Set the output folder and name of file to save generated astrological data
if("SUCCESS" == jsm.set_output(path="output", filename="swami_vivekananda_chart")):
    print(f'The output is : {jsm.get_output()}')
else:
    print("Given folder path doesnt exist")

############# Computing Astrological data ###############

if(jsm.reset_astrologicalData() == "SUCCESS"):  #Resetting the astrological data to clear history
    jsm.generate_astrologicalData(birthdata)    #Compute the astrological data based on new set.


print("✅ Chart generation completed successfully!")
print("📄 Astrological data saved to:", jsm.get_output())
print()
print("The generated chart includes:")
print("- D1 (Rashi) chart and all 15 divisional charts (D2-D60)")
print("- Planetary positions with exact nirayana_long values")
print("- Vimshottari Dasha system")
print("- Shadbala (planetary strengths)")
print("- Ashtakavarga calculations")
print("- Complete panchanga details")
print()
print("=== Example Complete ===")
