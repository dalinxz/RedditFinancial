$url = $_REQUEST['url'];
$url = checkValues($url);
 
function checkValues($value)
{
$value = trim($value);
if (get_magic_quotes_gpc()) 
{
	$value = stripslashes($value);
}
$value = strtr($value, array_flip(get_html_translation_table(HTML_ENTITIES)));
$value = strip_tags($value);
$value = htmlspecialchars($value);
return $value;
}	
 
function fetch_record($path)
{
$file = fopen($path, "r"); 
if (!$file)
{
	exit("Problem occured");
} 
$data = '';
while (!feof($file))
{
	$data .= fgets($file, 1024);
}
return $data;
}
 
$string = fetch_record($url);
/// fecth title
$title_regex = "/<title-->(.+)&lt;\/title&gt;/i";
preg_match_all($title_regex, $string, $title, PREG_PATTERN_ORDER);
$url_title = $title[1];
 
/// fecth decription
$tags = get_meta_tags($url);
 
// fetch images
$image_regex = '/&lt;img[^&gt;]*'.'src=[\"|\'](.*)[\"|\']/Ui';
preg_match_all($image_regex, $string, $img, PREG_PATTERN_ORDER);
$images_array = $img[1];
 
<div class="images">
$k=1;
for ($i=0;$i<=sizeof($images_array);$i++)
{
	if(@$images_array[$i])
	{
		if(@getimagesize(@$images_array[$i]))
		{
			list($width, $height, $type, $attr) = getimagesize(@$images_array[$i]);
			if($width -->= 50 &amp;&amp; $height &gt;= 50 ){ echo "<img id="&quot;.$k.&quot;" src="&quot;.@$images_array[$i].&quot;" width="100" />"; $k++; } } } } ?&gt; <!--<img src="ajax.jpg"  alt="" />--> <input id="total_images" name="total_images" type="hidden" value="&lt;?php echo --$k?&gt;" /></div>
<div class="info"><label class="title"> <!--?php  echo @$url_title[0]; ?--> </label> <br clear="all" /><label class="url"> <!--?php  echo substr($url ,0,35); ?--> </label> <br clear="all" /><br clear="all" /><label class="desc"> <!--?php  echo @$tags['description']; ?--> </label> <br clear="all" /><br clear="all" /><label style="float: left;"><img id="prev" src="prev.png" alt="" /><img id="next" src="next.png" alt="" /></label> <label class="totalimg"> Total <!--?php echo $k?--> images </label> </div>