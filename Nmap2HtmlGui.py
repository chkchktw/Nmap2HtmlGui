
import lxml.etree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os

# 內建 nmap-bootstrap.xsl 樣式表
NMAP_BOOTSTRAP_XSL = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="utf-8" indent="yes" doctype-system="about:legacy-compat"/>
  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta name="referrer" content="no-referrer"/> 
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"/>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous"/>
        <link rel="stylesheet" href="https://cdn.datatables.net/1.10.19/css/dataTables.bootstrap.min.css" type="text/css" integrity="sha384-VEpVDzPR2x8NbTDZ8NFW4AWbtT2g/ollEzX/daZdW/YvUBlbgVtsxMftnJ84k0Cn" crossorigin="anonymous"/>
        <script src="https://code.jquery.com/jquery-3.3.1.js" integrity="sha384-fJU6sGmyn07b+uD1nMk7/iSb4yvaowcueiQhfVgQuD98rfva8mcr1eSvjchfpMrH" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js" integrity="sha384-rgWRqC0OFPisxlUvl332tiM/qmaNxnlY46eksSZD84t+s2vZlqGeHrncwIRX7CGp" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/1.10.19/js/dataTables.bootstrap.min.js" integrity="sha384-7PXRkl4YJnEpP8uU4ev9652TTZSxrqC8uOpcV1ftVEC7LVyLZqqDUAaq+Y+lGgr9" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
        <style>
          .target:before {
            content: "";
            display: block;
            height: 50px;
            margin: -20px 0 0;
          }
          @media only screen and (min-width:1900px) {
            .container {
              width: 1800px;
              }
          }
          .footer {
            margin-top:60px;
            padding-top:60px;
            width: 100%;
            height: 180px;
            background-color: #f5f5f5;
          }
          .clickable {
            cursor: pointer;
          }
          .panel-heading > h3:before {
            font-family: 'Glyphicons Halflings';
            content: "\e114"; /* glyphicon-chevron-down */
            padding-right: 1em;
          }
          .panel-heading.collapsed > h3:before {
            content: "\e080"; /* glyphicon-chevron-right */
          }
        </style>
        <title>Scan Report Nmap <xsl:value-of select="/nmaprun/@version"/></title>
      </head>
      <body>
        <nav class="navbar navbar-default navbar-fixed-top">
          <div class="container-fluid">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#"><span class="glyphicon glyphicon-home"></span></a>
            </div>
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
              <ul class="nav navbar-nav">
                <li><a href="#scannedhosts">Scanned Hosts</a></li>
                <li><a href="#onlinehosts">Online Hosts</a></li>
                <li><a href="#openservices">Open Services</a></li>
              </ul>
            </div>
          </div>
        </nav>
        <div class="container">
          <div class="jumbotron">
            <h1>Scan Report<br/><small>Nmap <xsl:value-of select="/nmaprun/@version"/></small></h1>
            <pre style="white-space:pre-wrap; word-wrap:break-word;"><xsl:value-of select="/nmaprun/@args"/></pre>
            <p class="lead">
              <xsl:value-of select="/nmaprun/@startstr"/> – <xsl:value-of select="/nmaprun/runstats/finished/@timestr"/><br/>
              <xsl:value-of select="/nmaprun/runstats/hosts/@total"/> hosts scanned.
              <xsl:value-of select="/nmaprun/runstats/hosts/@up"/> hosts up.
              <xsl:value-of select="/nmaprun/runstats/hosts/@down"/> hosts down.
            </p>
            <div class="progress">
              <div class="progress-bar progress-bar-success" style="width: 0%">
                <xsl:attribute name="style">width:<xsl:value-of select="/nmaprun/runstats/hosts/@up div /nmaprun/runstats/hosts/@total * 100"/>%;</xsl:attribute>
                <xsl:value-of select="/nmaprun/runstats/hosts/@up"/>
                <span class="sr-only"></span>
              </div>
              <div class="progress-bar progress-bar-danger" style="width: 0%">
                <xsl:attribute name="style">width:<xsl:value-of select="/nmaprun/runstats/hosts/@down div /nmaprun/runstats/hosts/@total * 100"/>%;</xsl:attribute>
                <xsl:value-of select="/nmaprun/runstats/hosts/@down"/>
                <span class="sr-only"></span>
              </div>
            </div>
          </div>
          <h2 id="scannedhosts" class="target">Scanned Hosts<xsl:if test="/nmaprun/runstats/hosts/@down > 1024"><small> (offline hosts are hidden)</small></xsl:if></h2>
          <div class="table-responsive">
            <table id="table-overview" class="table table-striped dataTable" role="grid">
              <thead>
                <tr>
                  <th>State</th>
                  <th>Address</th>
                  <th>Hostname</th>
                  <th>TCP (open)</th>
                  <th>UDP (open)</th>
                </tr>
              </thead>
              <tbody>
                <xsl:choose>
                  <xsl:when test="/nmaprun/runstats/hosts/@down > 1024">
                    <xsl:for-each select="/nmaprun/host[status/@state='up']">
                      <tr>
                        <td><span class="label label-danger"><xsl:if test="status/@state='up'"><xsl:attribute name="class">label label-success</xsl:attribute></xsl:if><xsl:value-of select="status/@state"/></span></td>
                        <td><a><xsl:attribute name="href">#onlinehosts-<xsl:value-of select="translate(address/@addr, '.', '-')"/></xsl:attribute><xsl:value-of select="address/@addr"/></a></td>
                        <td><xsl:value-of select="hostnames/hostname/@name"/></td>
                        <td><xsl:value-of select="count(ports/port[state/@state='open' and @protocol='tcp'])"/></td>
                        <td><xsl:value-of select="count(ports/port[state/@state='open' and @protocol='udp'])"/></td>
                      </tr>
                    </xsl:for-each>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:for-each select="/nmaprun/host">
                      <tr>
                        <td><span class="label label-danger"><xsl:if test="status/@state='up'"><xsl:attribute name="class">label label-success</xsl:attribute></xsl:if><xsl:value-of select="status/@state"/></span></td>
                        <td><a><xsl:attribute name="href">#onlinehosts-<xsl:value-of select="translate(address/@addr, '.', '-')"/></xsl:attribute><xsl:value-of select="address/@addr"/></a></td>
                        <td><xsl:value-of select="hostnames/hostname/@name"/></td>
                        <td><xsl:value-of select="count(ports/port[state/@state='open' and @protocol='tcp'])"/></td>
                        <td><xsl:value-of select="count(ports/port[state/@state='open' and @protocol='udp'])"/></td>
                      </tr>
                    </xsl:for-each>
                  </xsl:otherwise>
                </xsl:choose>
              </tbody>
            </table>
          </div>
          <script>
            $(document).ready(function() {
              $('#table-overview').DataTable();
            });
            $('#table-overview').DataTable( {
              "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ]
            });
          </script>
          <h2 id="onlinehosts" class="target">Online Hosts</h2>
          <xsl:for-each select="/nmaprun/host[status/@state='up']">
            <div class="panel panel-default">
              <div class="panel-heading clickable" data-toggle="collapse">
                  <xsl:attribute name="id">onlinehosts-<xsl:value-of select="translate(address/@addr, '.', '-')"/></xsl:attribute>
                  <xsl:attribute name="data-target">#<xsl:value-of select="translate(address/@addr, '.', '-')"/></xsl:attribute>
                <h3 class="panel-title"><xsl:value-of select="address/@addr"/><xsl:if test="count(hostnames/hostname) > 0"> - <xsl:value-of select="hostnames/hostname/@name"/></xsl:if></h3>
              </div>
              <div class="panel-body collapse in">
                <xsl:attribute name="id"><xsl:value-of select="translate(address/@addr, '.', '-')"/></xsl:attribute>
                <xsl:if test="count(hostnames/hostname) > 0">
                  <h4>Hostnames</h4>
                  <ul>
                    <xsl:for-each select="hostnames/hostname">
                      <li><xsl:value-of select="@name"/> (<xsl:value-of select="@type"/>)</li>
                    </xsl:for-each>
                  </ul>
                </xsl:if>
                <h4>Ports</h4>
                <div class="table-responsive">
                  <table class="table table-bordered">
                    <thead>
                      <tr>
                        <th>Port</th>
                        <th>Protocol</th>
                        <th>State<br/>Reason</th>
                        <th>Service</th>
                        <th>Product</th>
                        <th>Version</th>
                        <th>Extra Info</th>
                      </tr>
                    </thead>
                    <tbody>
                      <xsl:for-each select="ports/port">
                        <xsl:choose>
                          <xsl:when test="state/@state = 'open'">
                            <tr class="success">
                              <td title="Port"><xsl:value-of select="@portid"/></td>
                              <td title="Protocol"><xsl:value-of select="@protocol"/></td>
                              <td title="State / Reason"><xsl:value-of select="state/@state"/><br/><xsl:value-of select="state/@reason"/></td>
                              <td title="Service"><xsl:value-of select="service/@name"/></td>
                              <td title="Product"><xsl:value-of select="service/@product"/></td>
                              <td title="Version"><xsl:value-of select="service/@version"/></td>
                              <td title="Extra Info"><xsl:value-of select="service/@extrainfo"/></td>
                            </tr>
                            <tr>
                              <td colspan="7">
                                <a><xsl:attribute name="href">https://nvd.nist.gov/vuln/search/results?form_type=Advanced&amp;cves=on&amp;cpe_version=<xsl:value-of select="service/cpe"/></xsl:attribute><xsl:value-of select="service/cpe"/></a>
                                <xsl:for-each select="script">
                                  <h5><xsl:value-of select="@id"/></h5>
                                  <pre style="white-space:pre-wrap; word-wrap:break-word;"><xsl:value-of select="@output"/></pre>
                                </xsl:for-each>
                              </td>
                            </tr>
                          </xsl:when>
                          <xsl:when test="state/@state = 'filtered'">
                            <tr class="warning">
                              <td><xsl:value-of select="@portid"/></td>
                              <td><xsl:value-of select="@protocol"/></td>
                              <td><xsl:value-of select="state/@state"/><br/><xsl:value-of select="state/@reason"/></td>
                              <td><xsl:value-of select="service/@name"/></td>
                              <td><xsl:value-of select="service/@product"/></td>
                              <td><xsl:value-of select="service/@version"/></td>
                              <td><xsl:value-of select="service/@extrainfo"/></td>
                            </tr>
                          </xsl:when>
                          <xsl:when test="state/@state = 'closed'">
                            <tr class="active">
                              <td><xsl:value-of select="@portid"/></td>
                              <td><xsl:value-of select="@protocol"/></td>
                              <td><xsl:value-of select="state/@state"/><br/><xsl:value-of select="state/@reason"/></td>
                              <td><xsl:value-of select="service/@name"/></td>
                              <td><xsl:value-of select="service/@product"/></td>
                              <td><xsl:value-of select="service/@version"/></td>
                              <td><xsl:value-of select="service/@extrainfo"/></td>
                            </tr>
                          </xsl:when>
                          <xsl:otherwise>
                            <tr class="info">
                              <td><xsl:value-of select="@portid"/></td>
                              <td><xsl:value-of select="@protocol"/></td>
                              <td><xsl:value-of select="state/@state"/><br/><xsl:value-of select="state/@reason"/></td>
                              <td><xsl:value-of select="service/@name"/></td>
                              <td><xsl:value-of select="service/@product"/></td>
                              <td><xsl:value-of select="service/@version"/></td>
                              <td><xsl:value-of select="service/@extrainfo"/></td>
                            </tr>
                          </xsl:otherwise>
                        </xsl:choose>
                      </xsl:for-each>
                    </tbody>
                  </table>
                </div>
                <xsl:if test="count(hostscript/script) > 0">
                  <h4>Host Script</h4>
                </xsl:if>
                <xsl:for-each select="hostscript/script">
                  <h5><xsl:value-of select="@id"/></h5>
                  <pre style="white-space:pre-wrap; word-wrap:break-word;"><xsl:value-of select="@output"/></pre>
                </xsl:for-each>
                <xsl:if test="count(os/osmatch) > 0">
                  <h4>OS Detection</h4>
                  <xsl:for-each select="os/osmatch">
                    <h5>OS details: <xsl:value-of select="@name"/> (<xsl:value-of select="@accuracy"/>%)</h5>
                    <xsl:for-each select="osclass">
                      Device type: <xsl:value-of select="@type"/><br/>
                      Running: <xsl:value-of select="@vendor"/><xsl:text> </xsl:text><xsl:value-of select="@osfamily"/><xsl:text> </xsl:text><xsl:value-of select="@osgen"/> (<xsl:value-of select="@accuracy"/>%)<br/>
                      OS CPE: <a><xsl:attribute name="href">https://nvd.nist.gov/vuln/search/results?form_type=Advanced&amp;cves=on&amp;cpe_version=<xsl:value-of select="cpe"/></xsl:attribute><xsl:value-of select="cpe"/></a>
                      <br/>
                    </xsl:for-each>
                    <br/>
                  </xsl:for-each>
                </xsl:if>
              </div>
            </div>
          </xsl:for-each>
          <h2 id="openservices" class="target">Open Services</h2>
          <div class="table-responsive">
            <table id="table-services" class="table table-striped dataTable" role="grid">
              <thead>
                <tr>
                  <th>Address</th>
                  <th>Port</th>
                  <th>Protocol</th>
                  <th>Service</th>
                  <th>Product</th>
                  <th>Version</th>
                  <th>CPE</th>
                  <th>Extra info</th>
                </tr>
              </thead>
              <tbody>
                <xsl:for-each select="/nmaprun/host">
                  <xsl:for-each select="ports/port[state/@state='open']">
                    <tr>
                      <td><a>
                      <xsl:attribute name="href">#onlinehosts-<xsl:value-of select="translate(../../address/@addr, '.', '-')"/></xsl:attribute><xsl:value-of select="../../address/@addr"/>
                      <xsl:if test="count(../../hostnames/hostname) > 0"> - <xsl:value-of select="../../hostnames/hostname/@name"/></xsl:if></a></td>
                      <td><xsl:value-of select="@portid"/></td>
                      <td><xsl:value-of select="@protocol"/></td>
                      <td><xsl:value-of select="service/@name"/></td>
                      <td><xsl:value-of select="service/@product"/></td>
                      <td><xsl:value-of select="service/@version"/></td>
                      <td><xsl:value-of select="service/cpe"/></td>
                      <td><xsl:value-of select="service/@extrainfo"/></td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>
              </tbody>
            </table>
          </div>
          <script>
            $(document).ready(function() {
              $('#table-services').DataTable();
              $("a[href^='#onlinehosts-']").click(function(event){     
                  event.preventDefault();
                  $('html,body').animate({scrollTop:($(this.hash).offset().top-60)}, 500);
              });
            });
            $('#table-services').DataTable( {
              "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ]
            });
            
          </script>
        </div>
        <footer class="footer">
          <div class="container">
            <p class="text-muted">
              This report was generated with <a href="https://github.com/honze-net/nmap-bootstrap-xsl">Nmap Bootstrap XSL</a>.<br/>
              Licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons BY-SA</a>.<br/>
              Designed and built by Andreas Hontzia (<a href="https://www.twitter.com/honze_net">@honze_net</a>).<br/>
            </p>
          </div>
        </footer>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
"""

# 轉換函數
def transform_xml_to_html():
    # 取得使用者選擇的檔案
    xml_file = entry_xml.get()
    output_html = entry_html.get()

    if not xml_file or not output_html:
        messagebox.showerror("錯誤", "請選擇 XML 檔案和輸出 HTML 檔案")
        return

    if not os.path.exists(xml_file):
        messagebox.showerror("錯誤", f"找不到 XML 檔案：{xml_file}")
        return

    try:
        # 讀取 XML
        xml = ET.parse(xml_file)
        
        # 解析內建 XSLT
        xsl = ET.XML(NMAP_BOOTSTRAP_XSL.encode("utf-8"))
        transform = ET.XSLT(ET.ElementTree(xsl))

        # 轉換 XML
        result = transform(xml)

        # 寫入 HTML 檔案
        with open(output_html, "wb") as f:
            f.write(result)

        messagebox.showinfo("成功", f"轉換完成！已輸出為：\n{output_html}")

        # 啟用 "開啟 HTML" 按鈕
        btn_open_html.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("轉換失敗", f"錯誤：{e}")

# 選擇 XML 檔案
def select_xml_file():
    file_path = filedialog.askopenfilename(filetypes=[("Nmap XML Files", "*.xml"), ("All Files", "*.*")])
    if file_path:
        entry_xml.delete(0, tk.END)
        entry_xml.insert(0, file_path)

# 選擇輸出 HTML 檔案
def select_html_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")])
    if file_path:
        entry_html.delete(0, tk.END)
        entry_html.insert(0, file_path)

# 開啟 HTML 檔案
def open_html_file():
    output_html = entry_html.get()
    if os.path.exists(output_html):
        webbrowser.open(output_html)
    else:
        messagebox.showerror("錯誤", "找不到 HTML 檔案")

# 建立 GUI 視窗
root = tk.Tk()
root.title("Nmap XML 轉 HTML 工具")
root.geometry("500x250")

# 標題
tk.Label(root, text="Nmap XML 轉 HTML", font=("Arial", 14, "bold")).pack(pady=10)

# 選擇 XML 檔案
frame_xml = tk.Frame(root)
frame_xml.pack(pady=5, padx=10, fill="x")
tk.Label(frame_xml, text="選擇 Nmap XML 檔案:").pack(side="left")
entry_xml = tk.Entry(frame_xml, width=40)
entry_xml.pack(side="left", padx=5)
tk.Button(frame_xml, text="選擇", command=select_xml_file).pack(side="right")

# 選擇 HTML 檔案
frame_html = tk.Frame(root)
frame_html.pack(pady=5, padx=10, fill="x")
tk.Label(frame_html, text="輸出 HTML 檔案:").pack(side="left")
entry_html = tk.Entry(frame_html, width=40)
entry_html.pack(side="left", padx=5)
tk.Button(frame_html, text="選擇", command=select_html_file).pack(side="right")

# 轉換按鈕
tk.Button(root, text="轉換 XML → HTML", font=("Arial", 12), command=transform_xml_to_html).pack(pady=10)

# 開啟 HTML 按鈕（預設禁用）
btn_open_html = tk.Button(root, text="開啟 HTML 報告", font=("Arial", 12), command=open_html_file, state=tk.DISABLED)
btn_open_html.pack(pady=5)

# 啟動 GUI
root.mainloop()
