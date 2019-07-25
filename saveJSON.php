<?php
/**
 * Created by PhpStorm.
 * User: Matt Jaquiery
 * Date: 19/03/2019
 * Time: 10:28
 *
 */

/*
The $_POST[] array will contain a JSON string which decomposes into:
{
    metadata:
        studyId: study identifier (becomes eid below)
        studyVersion: study version
        idCode: participant id
    data:
        JSON string to write to file
    privateData:
        JSON string to write to a protected file
}

Data are saved in the ./data/[public|private]/raw directory as specified in the incoming metadata.

An JSON string is returned with the following properties:
{
    error: description of any error which occurred,
    code: response code,
    content: message
}

*/

//phpinfo();
//error_reporting(0);
error_reporting(E_ALL);
ini_set("display_errors", 1);
include("file_with_errors.php");
ini_set("display_errors", true);
ini_set("auto_detect_line_endings", true);
$log = "";

function sulk($err, $code) {
    $out = array(
        "error" => $err,
        "code" => $code,
    );
    die(json_encode($out));
}


// Unpack POST data
$tmp = file_get_contents("php://input");
$tmp2 = parse_str($tmp,$json);
$json = json_decode($json["data"],true);

$id = (string) $json["participantId"][0]; 

//$meta = $json["metadata"];
//$data = $json["data"];
//$privateData = $json["privateData"];

//$eid = (string) $meta["studyId"];
// $version = (string) $meta["studyVersion"];
// $version = str_replace(".", "-", $version);
//$pid = $meta["idCode"];

// Check input is valid
// function is_alphanumeric($str, $allowHyphen = false) {
//     if($allowHyphen)
//         return (bool) preg_match('/^[0-9a-z\-]+$/i', $str);
//     return (bool) preg_match('/^[0-9a-z]+$/i', $str);
// }

// if(!is_alphanumeric($version, true))
//     sulk("Invalid version format '$version'.", 403);

// if(!is_alphanumeric($pid))
//     sulk("Invalid id '$pid'.", 403);

// if(!is_alphanumeric($eid, true)) {
//     sulk("Invalid studyId '$eid'.", 403);
// }

const PATH = "./data/public/";
$body = date('Y_m_d_H_i_s') . "_" . $id;

    $filename = PATH . $body . ".json";
    // if($privacy == "private")
    //     $write = $privateData;
    // else
    //     $write = $data;

    $empty = false;

    if(!$empty) {
        if (!file_exists($filename)) {
            try {
                $handle = fopen($filename, "w+b");
                // while (($data = fread($tmp, 1024)) !== FALSE) 
                // {
                //     fwrite($handle, stripslashes(json_encode($json)));
                // }   
                stream_copy_to_stream(stripslashes(json_encode($json)), $handle);
                fclose($handle);
            }
            catch (Exception $e)
            {
                echo 'Caught exception: ',  $e->getMessage(), "\n";
                sulk("Unable to create file.", 500);
            }
        } else
            sulk("File already exists!", 500);
    }
//}

// Send back the all clear
die(json_encode(array(
    "error" => "",
    "code" => 200,
    "content" => "Data saved successfully."
)));
