<?	

function char2hex($text){//из символа в хекс
$value = unpack('H*', $text);
return base_convert($value[1], 16, 16);
  }
function hexbin($hex){ 
   $bin=''; 
   for($i=0;$i<strlen($hex);$i++) 
       $bin.=str_pad(decbin(hexdec($hex{$i})),4,'0',STR_PAD_LEFT); 
      return $bin; 
} 
function hex2bin($str) {
    $bin = "";
    $i = 0;
    do {
        $bin .= chr(hexdec($str{$i}.$str{($i + 1)}));
        $i += 2;
    } while ($i < strlen($str));
    return $bin;
}
function bin2bstr($input)//из бинарных в текстовые
// Convert a binary expression (e.g., "100111") into a binary-string
{
  if (!is_string($input)) return null; // Sanity check
  // Pack into a string
  return pack('H*', base_convert($input, 2, 16));
}
// Returns string(3) "ABC"
//var_dump(bin2bstr('01000001 01000010 01000011'));
// Returns string(24) "010000010100001001000011"
//var_dump(bstr2bin('ABC'));
function bstr2bin($input)//из текстовых в бинарные
// Binary representation of a binary-string
{
  if (!is_string($input)) return null; // Sanity check
  // Unpack as a hexadecimal string
  $value = unpack('H*', $input);
  // Output binary representation
  return base_convert($value[1], 16, 2);
}

echo bstr2bin('XOR');
//echo bstr2bin('BCL');echo bstr2bin('XE\\');echo bstr2bin('KDE');
echo '
';
//echo bin2bstr('10110 00100111 11010010');

?>
