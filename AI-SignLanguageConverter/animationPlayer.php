        <div style="box-sizing: border-box; width: 30%; height: 80%; padding: 15px; float:right; margin-right:14%;" >
            <table align="center" style="width:100%; height:100%;" >
                <tr align="center">
                    <!--================================================================-->
                    <!-- CWA signing avatar panel 0 -->
                    <!--================================================================-->
                    <!-- Replaced by an avatar panel -->
                    <!--================================================================-->
                    <td width="100%" height="90%" >
                       <div class="CWASAAvatar av0" align="center" ></div>
                    </td>
                    <!--================================================================-->


                </tr>
                <tr>
                	<td>
                		<p class="alert-warning text-center" style="padding:5px; font-size:20px; font-weight:bold;" id="textHint"></p>
                	</td>             
                </tr>
                <tr style="display:none;">
                    <td align="center">
                        <span class="CWASAAvMenu av0" ></span>
                        <input type="button" value="Sign" class="bttnPlaySiGMLURL av0" />
                        <input type="button" value="Stop" class="bttnStop av0" />
                        <span class="CWASASpeed av0" ></span>
                        <br/>
                        <span style="font-size: 90%;" >
Sign/Frame:

                            <input class="txtSF av0" value="0/0" type="text">
Gloss:

                            <input class="txtGloss av0" value="[none]" type="text">
                        </span>
                        <!--  CachedSiGML URL  -->
                        <input type="text" id="URLText" class="txtSiGMLURL av0 undisplayed" value="" />
<script language="text/javascript">
// Set default sign
setSiGMLURL("SignFiles/hello.sigml");
</script>
                    </td>
                </tr>
            </table>
        </div>
