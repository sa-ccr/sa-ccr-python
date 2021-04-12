# sa-ccr-python

DISCLAIMER: Apart from being licensed in GPL, this version is far behind the level of the code contained in the SACCR R package, please contact us at info@openriskcalculator.com in case you would like any support in upgrading this.

This repository contains a prototype implementation of the Basel III Standardized Approach for Counterparty Credit Risk Management. (you can view the regulation here: http://www.bis.org/publ/bcbs279.htm)

A few words about the code:

The trade structure is based on an Object Oriented Hierarchy where the Trade class contains methods which apply for the all the trade types. For example, for the calculation of the supervisory delta, the supervisory duration etc a polymorphic method from the Trade class is being called.

The calcAddon function performs all the necessary groupings and aggregations per netting set and returns the aggregate Addon amount.
The supervisory factors values are being read through a csv file.
All the examples of the regulatory paper have been implemented (ExampleIRD.R contains the code for the IRDs case etc)
Features like maturity depending on the underlying, base transactions etc are not implemented in the open source version.

If you want to become a contributor to the project or use this code for commercial purposes or for any other queries please contact us at info@openriskcalculator.com or visit our website www.openriskcalculator.com

# Donate 

If you have found this software of use, please consider supporting us by donating below:

<table border="0" cellpadding="10" cellspacing="0" align="left"><tr><td align="left"></td></tr><tr><td align="left"><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SRBWEQJYJ8QM4&source=url" title="Donate via Paypal" onclick="javascript:window.open('https://www.paypal.com/webapps/mpp/paypal-popup','WIPaypal','toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=1060, height=700');"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/AM_SbyPP_mc_vs_dc_ae.jpg" border="0" alt="PayPal Acceptance Mark"></a></td></tr></table>


