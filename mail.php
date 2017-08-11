<?php

include 'connection.inc';

/* Begin Code */
function format()
{
		$args = func_get_args();
		if (count($args) == 0) {
				return;
		} //count($args) == 0
		if (count($args) == 1) {
				return $args[0];
		} //count($args) == 1
		$str = array_shift($args);
		$str = preg_replace_callback('/\\{(0|[1-9]\\d*)\\}/', create_function('$match', '$args = ' . var_export($args, true) . '; return isset($args[$match[1]]) ? $args[$match[1]] : $match[0];'), $str);
		return $str;
}


//-----------------------------------------Function to send mail starts---------------------//
/*function send_mail_attachment($from, $to, $cc, $bcc, $subject, $message, $file) {
// $file should include path and filename
/* $filename = basename($file);
$file_size = filesize($file);
$content = chunk_split(base64_encode(file_get_contents($file))); 
$uid = md5(uniqid(time()));
$from = str_replace(array("\r", "\n"), '', $from); // to prevent email injection
$header = "From: ".$from."\r\n"
."Cc: ".$cc."\r\n"
."Bcc: ".$bcc."\r\n"
."MIME-Version: 1.0\r\n"
."Content-Type: multipart/mixed; boundary=\"".$uid."\"\r\n\r\n"
."This is a multi-part message in MIME format.\r\n" 
."--".$uid."\r\n"
."Content-type: text/html; charset=UTF-8; format=flowed\r\n"
."Content-Transfer-Encoding: 7bit\r\n\r\n"
.$message."\r\n\r\n"
."--".$uid."\r\n"
."Content-Type: application/octet-stream; name=\"".$filename."\"\r\n"
."Content-Transfer-Encoding: base64\r\n"
."Content-Disposition: attachment; filename=\"".$filename."\"\r\n\r\n"
.$content."\r\n\r\n"
."--".$uid."--"; 
return mail($to, $subject, "", $header);
}*/
//---------------------------End of Function to send mail ----------------------------//


/*----------------------------------------- main mail send fuction ---------------------------------*/
function mail_html($mailto, $from_mail, $from_name, $replyto, $subject, $message)
{
		//$from_detail = $from_name.'<'. $from_mail .'>';
		$header = "";
		$header .= "From:".$from_mail. "\r\n";
		$header .= "Reply-To: " . $replyto . "\r\n";
		$header .= "Return-Path: bounce-mail@fossee.in"."\r\n"; // needs to be changed acording to foss
		//$header .= "Message:" .$message . "\r\n\r\n";
		$header .= "MIME-Version: 1.0"."\r\n";
		$header .= "Content-type: text/html; charset=iso-8859-1" ."\r\n";
		return mail($mailto, $subject, $message,$header,"-fbounce-mail@fossee.in"); // needs to be changed according to foss
}

/*****************used to send mail with attachment *********************/
/*
function mail_html($mailto, $from_mail, $from_name, $replyto, $subject, $message, $attachment) {
$filename1 = basename($attachment1);
$file_size1 = filesize($attachment1);
$content1 = chunk_split(base64_encode(file_get_contents($attachment1))); 
$filename2 = basename($attachment2);
$file_size2 = filesize($attachment2);
$content2 = chunk_split(base64_encode(file_get_contents($attachment2)));
$files = $attachment;
$uid = md5(uniqid(time()));
$header = "From: ".$from_mail."\r\n";
$header .= "Reply-To: ".$replyto."\r\n";
$header .= "Return-Path: bounce-mail@fossee.in";
$header .= "MIME-Version: 1.0 \r\n";
//  $header .= "Content-type: text/html; charset=iso-8859-1 \r\n";
$header .= "Content-Type: multipart/mixed; boundary=\"".$uid."\"\r\n\r\n";
$header .= "This is a multi-part message in MIME format.\r\n"; 
$header .= "--".$uid."\r\n";
$header .= "Content-type: text/html; charset=UTF-8; format=flowed\r\n";
$header .= "Content-Transfer-Encoding: 7bit\r\n\r\n";
$header .= $message."\r\n\r\n";
$header .= "--".$uid."\r\n";
// preparing attachments
for($x=0;$x<count($files);$x++){
$filesloc="/home/prashant/".$files[$x]; //Change it with your file location.This must be your server path not url path
$file = fopen($filesloc,"rb");
$data = fread($file,filesize($filesloc));
fclose($file);
$data = chunk_split(base64_encode($data));
$header .= "Content-Type: {\"application/octet-stream\"};\n" . " name=\"$files[$x]\"\n" .
"Content-Disposition: attachment;\n" . " filename=\"$files[$x]\"\n" .
"Content-Transfer-Encoding: base64\n\n" . $data . "\n\n";
$header .= "--".$uid."\n";
}
// $header .= $message."\r\n\r\n";
return mail($mailto, $subject, "", $header, "-fbounce-mail@fossee.in");
}
*/
//--------------------------------------------End of Function to send mail with attachment-----------------//

/*----------------------------------------Fucntion to generate a random string----------------------------*/
function generateRandomString($length = 33)
{
		$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
		$charactersLength = strlen($characters);
		$randomString = '';
		for ($i = 0; $i < $length; $i++) {
				$randomString .= $characters[rand(0, $charactersLength - 1)];
		} //$i = 0; $i < $length; $i++
		return $randomString;
}
/*----------------------------------------Fucntion to generate a random string ends----------------------------*/

//$invite = file_get_contents('spoken-tutorial-project-research-assistant-p-14-29.txt');
//$attachment =array( "Fossee_Optimization_Toolbox_for_Scilab.pdf");
//$invite = file_get_contents('/Site/fossee_drupal/data/emails/scipy_conference_2016_invite.html');
//$invite = file_get_contents('scilab-toolbox-workshop-2-dec.txt');
//$invite = file_get_contents('/Site/fossee_drupal/data/emails/fossee_jobs_2016_notification.html');

//$invite = file_get_contents('scilab_arduino_workshop_2015_invite.html');
//$invite = file_get_contents('/Site/fossee_drupal/data/emails/fossee_laptop_precausions_2015.html');
//$invite = file_get_contents('/Site/fossee_drupal/data/emails/cfd_openfoam_symposium_2016_invite.html');
//$invite = file_get_contents('/Site/fossee_drupal/data/emails/osdag_workshop_2016_invitation.html');
//$invite = file_get_contents('/Site/fossee_drupal/data/emails/esim_workshop_june_2016.html');
//$invite = file_get_contents('esim_workshop_certificate_mail.html');
//$invite = file_get_contents('toolbox_mail_content.txt');

/*$invite = "
<!DOCTYPE html>
<html>
<body>
Dear Participant,
<br><br>
Please follow the instructions given at the following link to install the required software: <a href='http://fossee.in/workshop/Scilab-Arduino/#install'>http://fossee.in/workshop/Scilab-Arduino/#install</a>
<br>
<strong style = 'color:red'>*</strong> It is mandatory to bring your laptop along with the software listed, to be able to participate in the workshop.

<br> <br>
Regards,
<br>
Scilab-Arduino Team,<br>
<a href='http://fossee.in'>FOSSEE</a>, <a href='http://www.iitb.ac.in'> IIT Bombay</a>.
</body>
</html>

";*/

/*$invite = '
<!DOCTYPE html>
<html>
<body>

<p>Dear Participant [{0}],<br />
<br />
Please find attached <strong>pdf file with the instructions</strong> to install required packages for the workshops.</p>

<div>Make sure you install all the mentioned packages prior to your visit for the conference.<br />
<br />
Please refer the following link for some general instructions &amp; directions to help you during your stay at IIT Bombay<br />
<a href="http://fossee.in/data/emails/Instructions-for-SciPy-India-2015-Conference.pdf" target="_blank">http://fossee.in/data/emails/Instructions-for-SciPy-India-2015-Conference.pdf</a><br />
&nbsp;</div>

<div>Regards,</div>

<p>SciPy India team</p>
</body>
</html>

';*/


/******************************mail content for scipy certificate **********************/
/*
$invite = "
<!DOCTYPE html>
<html>
<body>

<p>Dear Participant [{0}],<br />
<br />
<div>Thank you for attending OpenModelica Workshop 2017. Your participation certificate for the workshop is now ready.</div>

<div>&nbsp;</div>

<div>Please visit this link to download your certificate: <a href='http://fossee.in/certificates/openmodelica_feedback_2017/' target='_blank'>http://fossee.in/certificates/openmodelica_feedback_2017/</a></div>

<div>&nbsp;</div>

<div>We also request you to provide your valuable feedback on the workshop.</div>

<div>&nbsp;</div>

<div>Regards,</div>

<p>OpenModelica team,
<br>
<a href='http://fossee.in' target='_blank'>FOSSEE</a>, IIT Bombay

</p>


</body>
</html>

";
*/


/******************************mail content for scipy certificate **********************/
/*$invite = "
<!DOCTYPE html>
<html>
<body>

<p>Dear Sir/Ma'am [{0}],<br />
<br />
<div>The FOSSEE group is pleased to announce the FOSSEE Summer Internship 2017 Program. FOSSEE group promotes the use of various open source tools for academic and research purposes. Interns will get an opportunity to apply their knowledge and skills in developing cutting edge open source tools. Internships are available for both undergraduate and graduate students and all positions are paid. </div>

<div>&nbsp;</div>

<div>For more details, please visit- <a href='http://fossee.in/jobs' target='_blank'>http://fossee.in/jobs</a>. The application deadline is 5 PM, Feb. 28, 2017
. </div>

<div>&nbsp;</div>

<div>Please forward this email to your students, colleagues, friends and anyone who would interested in participating in this internship.</div>

<div>&nbsp;</div>

<div>Regards,</div>

<p>Shamika,
<br>
<a href='http://fossee.in' target='_blank'>FOSSEE</a>, IIT Bombay

</p>


</body>
</html>

";
*/
/***************************************************************************************/

/*$invite = "
<!DOCTYPE html>
<html>
<body>
Dear Participant,
<br><br>
Greetings from FOSSEE, IIT Bombay!
<br><br>
1) To enter the campus, you will be required to present a valid ID proof along with the Scilab-Arduino workshop ticket that we issued.
<br><br>
2) Once you reach IIT Bombay campus, please proceed to Hostel No.15 (Females) and Hostel No.16 (Males). On your arrival at the hostel, please meet the Hall-Manager / Security who shall allot you the room.
<br><br>
<table border = '1'>
<tr style ='font-weight:bold;background-color:#3166ff;color:#000000;text-align:center'>
<th colspan='2'>Hostel Address</th>
</tr>
<tr>
<td>Hostel 15 C-Wing (Females)</td>
<td>Hostel 16 (Males)</td>
</tr>
<tr>
<td>Near SAMEER, Hill side, IIT Bomaby,Mumbai, Maharashtra 400076</td>
<td>Near SAMEER, Hill side, IIT Bomaby, Mumbai, Maharashtra 400076</td>
</tr>
<tr>
<td>Hall Manager: 022-2576-2715 <br>Security: 022-2576-2615</td>
<td>Hall Manager: 022-2576-2716 <br>Security: 022-2576-2616</td>
</tr>
</table>
<br><br>
For any queries that you may have, please feel free to call us on:
022-2576-4111 (10:00 AM to 06:00 PM).
<br><br>
<strong style = 'color:red'>*</strong> Please visit the workshop website (<a href = 'http://fossee.in/workshop/Scilab-Arduino/'>http://fossee.in/workshop/Scilab-Arduino/</a>) for directions to reach the hostels / venue and for other instructions.
<br><br>
Thanks and Regards,
<br>
Scilab-Arduino Team,<br>
<a href='http://fossee.in'>FOSSEE</a>, <a href='http://www.iitb.ac.in'> IIT Bombay</a>.
</body>
</html>

";*/
/*$invite = '

<!DOCTYPE html>
<html>
<body>
<p><span style="color: #000000;">Dear Candidate,<br /><br /><br />You are receiving this notification as you have previously applied for a position at FOSSEE, IIT Bombay.<br /><br />We are glad to inform you that we have new openings for multiple positions in the project. For further details and for applications, please visit: <a href="http://www.ircc.iitb.ac.in/IRCC-Webpage/rnd/JobOpportunities.jsp" target="_blank">http://fossee.in/jobs</a><br /><br />Direct link to the notification:<br /><a href="http://www.ircc.iitb.ac.in/IRCC-Webpage/Circular/B-38_P14_16-17.pdf" target="_blank">http://www.ircc.iitb.ac.in/IRC<wbr />C-Webpage/Circular/B-38_P14_<wbr />16-17.pdf</a><br /><br /><br />Regards,<br /></span></p>
<div>
<div class="m_-4465076580529478737m_-640973387023458399gmail_signature">
<div dir="ltr">
<div>
<div dir="ltr">
<div>
<div dir="ltr">
<div>
<div dir="ltr">
<div>
<div dir="ltr">
<div>
<div dir="ltr">
<div>
<div dir="ltr">
<div><span style="color: #0000ff;"><a href="http://fossee.in" target="_blank">FOSSEE</a><strong>,</strong><br /><a href="http://iitb.ac.in" target="_blank">IIT Bombay</a><span style="background-color: #073763;"><span style="background-color: #073763;"><span style="background-color: #ffffff;">.</span></span></span></span></div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>

</body>
</html>
';
*/
/*$invite = "<!DOCTYPE html>
<html>
<body>
Dear Participant,
<br><br>
<h4>Please make note of the following points:</h4><br>
<ul>
<li> Installing software required for the workshop is not supported at the venue. You are required to install all the software prior to attending the workshop. Visit: <a href = 'http://fossee.in/workshop/Scilab-Arduino/#install'>http://fossee.in/workshop/Scilab-Arduino/#install</a></li>

<li> Internet connection shall not be provided at the venue and at the hostels. You are requested to make your own arrangements for the same.</li>

<li> A headphone/earphone is required for video tutorials.</li>

<li> A pen-drive is recommended for exchanging of intermediate files (if any) during the course of the workshop.</li>

<li> There is no warranty on the hardware (Arduino Uno board, sensor shield, DC motor) provided, after workshop.</li>

<li> Participant should report any functional issues with hardware on the first day of the workshop.</li>

<li> Physical damage, short-circuit to the hardware does not qualify for replacement. </li>

<li> E-certificate of participation shall be available for download from 13 July, 10 A.M onwards. Link to the same will be notified to your registered email.</li>
</ul>
<p>
Please find the attached quick-information.pdf file. You are recommended to carry a copy of this sheet for handy information.</p>
<br><br>
Thanks and Regards,
<br>
Scilab-Arduino Team,<br>
<a href='http://fossee.in'>FOSSEE</a>, <a href='http://www.iitb.ac.in'> IIT Bombay</a>.
</body>
</html>
";*/
//$attachment =array( "esim-brochure.pdf","sandhi-brochure.pdf");

/*$invite = "<p>Dear {0},</p>

<p>We are sorry for the inconvenience caused with respect to downloading the Python TBC certificates. The issue is resolved and now you may download your certificates.</p>

<p>If you had already downloaded and if it is not for you, please ignore this email.</p>

<p>Regards,<br />
Python TBC</p>

";
*/

$i = 1;
//$sql = "SELECT email FROM test_email";
//$result = $conn->query($sql);
$stmt = $conn->prepare('SELECT * FROM test_email WHERE active=1');
//$stmt = $conn->prepare('SELECT * FROM scipy_invitation_list_2015');
//$stmt = $conn->prepare('SELECT * FROM scipy_attendee_list_certificate');
//$stmt = $conn->prepare('SELECT * FROM 4last_4k');
//$stmt = $conn->prepare('SELECT * FROM python_cordinator_email_list_kiran_5_10_2015');
//$stmt = $conn->prepare('SELECT * FROM python_cordinator_email_list_usha_9_11_2015');
//$stmt = $conn->prepare("SELECT email FROM `sent_email` WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$' AND event != 'scipy-in-2016-invitation'");
//$stmt = $conn->prepare("SELECT email FROM `institute_email_id_esim` WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");
//$stmt = $conn_scilab->prepare("SELECT mail as email FROM `users` WHERE `mail` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");
//$stmt = $conn_esim->prepare("SELECT mail as email FROM `users` WHERE `mail` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");
//$stmt = $conn_cfd->prepare("SELECT mail as email FROM `users` WHERE `mail` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");

//$stmt = $conn->prepare("SELECT email as email FROM `python_tbc_auth_user` WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");

//$stmt = $conn->prepare('SELECT * FROM esim_participant_list');
//$stmt = $conn->prepare('SELECT * FROM osdag_workshop_participant_list');
//$stmt = $conn->prepare('SELECT email FROM scilab_user_10_3_2016');
//$stmt = $conn->prepare('SELECT name, email FROM osdag_workshop_2016_invite_industries_psu WHERE sent = 0 AND registred = 0');
//$stmt = $conn->prepare('SELECT name, email FROM osdag_workshop_2016_invite WHERE sent = 0 AND registred = 0');
//$stmt = $conn->prepare('SELECT email FROM esim_workshop_june_2016_invite_email_list WHERE sent = 1');
//$stmt = $conn_college_address->prepare("SELECT email as email FROM `email_address_college`  WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");
//$stmt = $conn->prepare('SELECT email FROM gujarat_college_email_id_vineeta_3_june_2016 WHERE sent = 0');
//$stmt = $conn->prepare('SELECT * FROM job_notification');
//$stmt = $conn->prepare('SELECT email FROM tpo_email');
//$stmt = $conn->prepare('SELECT * FROM `applications-spoken-tutorial-p-14-26-project-technical-assistant`');
//$stmt = $conn->prepare('SELECT * FROM `applications-p-14-17-shortlisted`');
//$stmt = $conn->prepare('SELECT * FROM `scipyinvitation_kiran_9_nov_2016`');
//$stmt = $conn->prepare("SELECT email as email FROM `scilab_fot_workshop_email_pune` WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");
//$stmt = $conn->prepare("SELECT email as email FROM `openmodelica_workshop_email_jan2017` WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");
//$stmt = $conn->prepare("SELECT email as email FROM `generic-iot` WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");
//$stmt = $conn->prepare("SELECT email as email FROM `generic-iot-onlinetest` WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");
//$stmt = $conn->prepare("SELECT email as email FROM `SBHS-Simulation-RT-Lab-intern-list` WHERE `email` REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'");


$stmt->execute();
$result_count = $stmt->rowCount();
$invite = file_get_contents('fossee_newsletter4.html');
//$invite = file_get_contents('spoken-tutorial-project-technical-assistant-p-14-26.txt');

if ($result_count > 0) {
		
		// output data of each row
		while ($data = $stmt->fetchAll(PDO::FETCH_ASSOC)) {
				foreach ($data as $row) {
						$hash_string = generateRandomString();
						//$event = 'osdag-workshop-2016-invitation';
						//$event = 'eSim-workshop-june-2016-invitation';
						//$event = 'eSim-workshop-june-2016-certificate-notification';
						//$event = 'osdag-workshop-june-2016-certificate-notification';
						//$event = 'scilab-toolbox-test-notification';
						//$event= 'scipy-in-2016-invitation';
						//$event= 'scilab-toolbox-workshop-2-dec-16';
						//$event= 'fossee-summer-internship-2017-iot-onlinetest';
						//$event = 'fossee-summer-internship-2017-sbhs';
						//$event='fossee-newsletter';
						$event='python-workshop-invitation';
						//$event= 'openmodelica-workshop-jan2017';
						//$event= 'job-interview-p14-26-project-technical-assistant-notification1';
						//$event= 'job-interview-p14-17-shortlisted-notification1';
						$hash_key = urlencode($hash_string);
						$hash = $hash_key . '&event=' . $event;
						// $unsub_link = 'http://fossee.in/data/emails/unsubscribe-fossee-laptop-notification.php?key='. $hash;
						$unsub_link = 'http://fossee.in/data/emails/unsubscribe.php?key=' . $hash;
						//$unsub_link = 'http://fossee.in/data/emails/unsubscribe-fossee-job-alert.php?key=' . $hash;
						//$unsub_link = 'http://fossee.in/data/emails/unsubscribe.php?key=' . $hash;
						$em = trim(strtolower($row['email']));
						//$em = "sushanth.g@christuniversity.in";
						$ar = explode("@", $em);
						//$firstname = $ar[0];
						//$name = $row['name'];
						//$firstname = trim(ucwords(strtolower($name)));
						$firstname = $em;
						//$firstname = $row['name']; //enable when name are provided with email list
						$message = format($invite, $firstname, $unsub_link);
						// mail_html($em, 'toolbox@scilab.in', 'Scilab Team - FOSSEE, IIT Bombay', 'toolbox@scilab.in', ' Test Scilab Optimization Toolbox', $message, $attachment);
						//mail_html($em, 'laptop@fossee.in', 'FOSSEE Admin', 'laptop@fossee.in', 'FOSSEE Laptop Precautions', $message);
						if ($i > 0 && $i % 10 == 0) {
								sleep(5);
								
						} //$i > 0 && $i % 10 == 0
						//mail_html($mailto, $from_mail, $from_name, $replyto, $subject, $message, $attachment) 
						//mail_html($em, 'scipy@fossee.in', 'SciPy India Conference 2015', 'scipy@fossee.in', 'SciPy India 2015 - Installation instructions for the workshops', $message, $attachment);
						//mail_html($em, 'contact-cfd@fossee.in', 'OpenFOAM Symposium 2016', 'contact-cfd@fossee.in', 'OpenFOAM Symposium 2016 - Invitation', $message, $attachment);
						//mail_html($em, 'toolbox@scilab.in', 'Scilab Toolbox Testing', 'toolbox@scilab.in', 'Coders / Testers for Scilab Toolboxes', $message);
						//mail_html($em, 'info@fossee.in', 'FOSSEE Internship', 'info@fossee.in', 'Internship Certificate', $message);
						//mail_html($em, 'contact-osdag@fossee.in', 'Prof. Siddhartha Ghosh', 'contact-osdag@fossee.in', 'Invitation - Osdag Workshop 2016', $message);
						//mail_html($em, 'contact-esim@fossee.in', 'eSim Team - FOSSEE', 'contact-esim@fossee.in', 'Invitation - eSim Workshop 2016', $message);
						 //mail_html($em, 'contact-esim@fossee.in', 'eSim Team - FOSSEE', 'contact-esim@fossee.in', 'Notification - eSim Workshop June 2016', $message);
						//mail_html($em, 'contact-osdag@fossee.in', 'Osdag Team - FOSSEE', 'contact-osdag@fossee.in', 'Notification - Osdag Pre-Launch Workshop June 2016', $message);
 
$stmt_check = $conn->prepare('SELECT * FROM sent_email WHERE email= :email AND event=:event and counter>1');
$stmt_check->execute(array('event' => $event,'email'=>$row['email']));
$result_count_check = $stmt_check->rowCount();
//print $result_count_check;die;
if($result_count_check == 0){
sleep(2);
						//mail_html($em, 'scipy@fossee.in', 'SciPy Team - FOSSEE', 'scipy@fossee.in', 'SciPy India Conference 2016', $message);
						//mail_html($em, 'toolbox@scilab.in', 'FOSSEE Team, IIT Bombay', 'toolbox@scilab.in', 'FOSSEE Summer Internship- Generic IoT Platform', $message);
						//mail_html($em, 'toolbox@scilab.in', 'FOSSEE Team, IIT Bombay', 'toolbox@scilab.in', 'FOSSEE Summer Internship- Generic Platform for IoT- Online Test', $message);
						//mail_html($em, 'sbhs@os-hardware.in', 'FOSSEE Team, IIT Bombay', 'sbhs@os-hardware.in', 'FOSSEE Summer Internship- SBHS Simulation RT Lab- Problem Statement', $message);
						mail_html($em, 'info@fossee.in', 'FOSSEE Team, IIT Bombay', 'info@fossee.in', 'FOSSEE Newsletter(Sample)', $message);
						// mail_html($em, 'info@fossee.in', 'Scilab Team - FOSSEE', 'contact@scilab.in', 'FOSSEE Optimization Toolbox Workshop', $message);
						//mail_html($em, 'info@fossee.in', 'FOSSEE - IIT Bombay', 'jobs@fossee.in', 'FOSSEE / Spoken Tutorial Recruitment: Online Screening Test on 3 Nov 2016', $message);
						//mail_html($em, 'info@fossee.in', 'FOSSEE - IIT Bombay', 'jobs@fossee.in', 'FOSSEE Recruitment: Screening Assignment', $message);


						//$sql_in =$pdo->prepare('INSERT INTO sent_email(email, unsubscribe, email_hash, event) VALUES ('".$em."', 0,'".$hash."', 'scipy 2015')"; 
						$sql_in = $conn->prepare('INSERT INTO sent_email(email, unsubscribe, email_hash, event,counter) VALUES(:email, 0, :hash, :event, counter+1) ');
						//$result_in = $sql_in->execute(array('email' => $em,'hash'=>$hash, 'event'=>'fossee laptop greetings'));
						$result_in = $sql_in->execute(array(
								'email' => $em,
								'hash' => $hash_string,
								'event' => $event
						));

			print "\e[1;32m\n" . $i . '=>' . $firstname . '=>' . $row['email'] . "\n";
            echo "";
            //sleep(2);
            $i++;
}else{
			print  "\e[1;31m\n". $i . '=>' . $firstname . '=>' . $row['email'] . "------ Already sent"."\e[1;32m\n";
            echo "";

}

					/*	
						$sent_sql_in = $conn->prepare('UPDATE esim_workshop_june_2016_invite_email_list SET sent = 1 WHERE email = :email');
						$sent_result_in = $sent_sql_in->execute(array(
                                          
					                      'email' => $em,
                                                ));
					*/
						/*$sent_sql_in = $conn->prepare('UPDATE college_email_id_fahim_27_06_2016 SET sent = 1 WHERE email = :email');
                                                $sent_result_in = $sent_sql_in->execute(array(
                                          
                                                              'email' => $em,
                                                ));
					*//*
						$sent_sql_in = $conn->prepare('UPDATE gujarat_college_email_id_vineeta_3_june_2016 SET sent = 1 WHERE email = :email');
                                                $sent_result_in = $sent_sql_in->execute(array(
                                          
                                                              'email' => $em,
                                                ));
						*/

                                           
					/*	$sent_sql_in = $conn->prepare('UPDATE osdag_workshop_2016_invite SET sent = 1 WHERE email = :email');
                                                $sent_result_in = $sent_sql_in->execute(array(
                                          
                                                              'email' => $em,
                                                ));
						
						$sent_sql_in = $conn->prepare('UPDATE osdag_workshop_2016_invite_industries_psu SET sent = 1 WHERE email = :email');
                                                $sent_result_in = $sent_sql_in->execute(array(

                                                              'email' => $em,
                                                ));
*/

						//$result_in = $conn->query($sql_in);
						//print $i . '=>' . $firstname . '=>' . $row['email'] . "\n";
						//echo "";
						//sleep(2);
						//$i++;
						
				} //$data as $row
		} //$data = $stmt->fetchAll(PDO::FETCH_ASSOC)
} //$result_count > 0
else {
		echo "0 results";
		
}
$conn = null;

?>
