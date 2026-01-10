' VBA MACRO TEMPLATE FOR RESUME JOB MATCHER
' Copy and paste these macros into Excel's VBA Editor (Alt+F11)
' These macros work with the exported job matches Excel file

' ============================================
' MACRO 1: Filter Jobs by Match Percentage
' ============================================
Sub FilterByMatch()
    Dim ws As Worksheet
    Dim matchThreshold As Integer
    Dim lastRow As Long
    Dim i As Long
    
    Set ws = ThisWorkbook.Sheets("Job Matches")
    matchThreshold = InputBox("Enter minimum match percentage (0-100):", "Filter Jobs", 50)
    
    If matchThreshold < 0 Or matchThreshold > 100 Then
        MsgBox "Invalid input. Please enter a value between 0 and 100."
        Exit Sub
    End If
    
    lastRow = ws.Cells(ws.Rows.Count, "E").End(xlUp).Row
    
    For i = 2 To lastRow
        If ws.Cells(i, 5).Value < matchThreshold Then
            ws.Rows(i).Hidden = True
        Else
            ws.Rows(i).Hidden = False
        End If
    Next i
    
    MsgBox "Filtered jobs with match >= " & matchThreshold & "%"
End Sub

' ============================================
' MACRO 2: Sort Jobs by Match Score
' ============================================
Sub SortByMatchScore()
    Dim ws As Worksheet
    Dim dataRange As Range
    Dim lastRow As Long
    
    Set ws = ThisWorkbook.Sheets("Job Matches")
    lastRow = ws.Cells(ws.Rows.Count, "E").End(xlUp).Row
    
    Set dataRange = ws.Range("A1:G" & lastRow)
    
    With ws.Sort
        .SortFields.Clear
        .SortFields.Add Key:=ws.Range("E1"), Order:=xlDescending
        .SetRange dataRange
        .Header = xlYes
        .Apply
    End With
    
    MsgBox "Jobs sorted by match score (highest first)"
End Sub

' ============================================
' MACRO 3: Highlight Top Matches
' ============================================
Sub HighlightTopMatches()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim matchValue As Double
    
    Set ws = ThisWorkbook.Sheets("Job Matches")
    lastRow = ws.Cells(ws.Rows.Count, "E").End(xlUp).Row
    
    For i = 2 To lastRow
        matchValue = ws.Cells(i, 5).Value
        
        If matchValue >= 70 Then
            ws.Rows(i).Interior.Color = RGB(200, 230, 201) ' Light green
        ElseIf matchValue >= 50 Then
            ws.Rows(i).Interior.Color = RGB(255, 249, 196) ' Light yellow
        ElseIf matchValue >= 30 Then
            ws.Rows(i).Interior.Color = RGB(255, 204, 188) ' Light orange
        End If
    Next i
    
    MsgBox "Top matches highlighted!"
End Sub

' ============================================
' MACRO 4: Export Current Sheet to CSV
' ============================================
Sub ExportToCSV()
    Dim ws As Worksheet
    Dim csvPath As String
    Dim fso As Object
    Dim csvFile As Object
    Dim lastRow As Long
    Dim lastCol As Long
    Dim i As Long
    Dim j As Long
    Dim csvLine As String
    
    Set ws = ActiveSheet
    csvPath = ThisWorkbook.Path & "\" & ws.Name & "_" & Format(Now(), "yyyymmdd_hhmmss") & ".csv"
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set csvFile = fso.CreateTextFile(csvPath, True)
    
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    
    For i = 1 To lastRow
        csvLine = ""
        For j = 1 To lastCol
            csvLine = csvLine & ws.Cells(i, j).Value
            If j < lastCol Then csvLine = csvLine & ","
        Next j
        csvFile.WriteLine csvLine
    Next i
    
    csvFile.Close
    MsgBox "Exported to: " & csvPath
End Sub

' ============================================
' MACRO 5: Generate Match Distribution Chart
' ============================================
Sub GenerateChart()
    Dim ws As Worksheet
    Dim chartSheet As Worksheet
    Dim chart As Object
    Dim dataRange As Range
    
    Set ws = ThisWorkbook.Sheets("Dashboard")
    
    ' Create new chart sheet
    Set chartSheet = ThisWorkbook.Sheets.Add
    chartSheet.Name = "Match Chart"
    
    ' Reference data from Dashboard
    Set dataRange = ws.Range("A16:B19")
    
    ' Create pie chart
    Set chart = chartSheet.Shapes.AddChart.Chart
    chart.ChartType = xlPie
    chart.SetSourceData dataRange
    chart.HasTitle = True
    chart.ChartTitle.Text = "Job Match Distribution"
    
    MsgBox "Chart created on 'Match Chart' sheet"
End Sub

' ============================================
' MACRO 6: Auto-Format All Sheets
' ============================================
Sub AutoFormatSheets()
    Dim ws As Worksheet
    Dim headerFill As Object
    Dim headerFont As Object
    
    For Each ws In ThisWorkbook.Sheets
        ' Format header row
        With ws.Rows(1)
            .Interior.Color = RGB(46, 125, 50) ' Green
            .Font.Bold = True
            .Font.Color = RGB(255, 255, 255) ' White
            .Font.Size = 12
            .HorizontalAlignment = xlCenter
        End With
        
        ' Auto-fit columns
        ws.Columns.AutoFit
    Next ws
    
    MsgBox "All sheets formatted!"
End Sub

' ============================================
' MACRO 7: Create Summary Statistics
' ============================================
Sub CreateSummaryStats()
    Dim ws As Worksheet
    Dim statsWs As Worksheet
    Dim lastRow As Long
    Dim totalJobs As Long
    Dim avgMatch As Double
    Dim maxMatch As Double
    Dim minMatch As Double
    Dim i As Long
    
    Set ws = ThisWorkbook.Sheets("Job Matches")
    lastRow = ws.Cells(ws.Rows.Count, "E").End(xlUp).Row
    totalJobs = lastRow - 1
    
    ' Calculate statistics
    avgMatch = 0
    maxMatch = 0
    minMatch = 100
    
    For i = 2 To lastRow
        avgMatch = avgMatch + ws.Cells(i, 5).Value
        If ws.Cells(i, 5).Value > maxMatch Then maxMatch = ws.Cells(i, 5).Value
        If ws.Cells(i, 5).Value < minMatch Then minMatch = ws.Cells(i, 5).Value
    Next i
    
    avgMatch = avgMatch / totalJobs
    
    ' Create or update stats sheet
    On Error Resume Next
    Set statsWs = ThisWorkbook.Sheets("Statistics")
    If statsWs Is Nothing Then
        Set statsWs = ThisWorkbook.Sheets.Add
        statsWs.Name = "Statistics"
    End If
    On Error GoTo 0
    
    statsWs.Range("A1").Value = "Job Match Statistics"
    statsWs.Range("A2").Value = "Total Jobs:"
    statsWs.Range("B2").Value = totalJobs
    statsWs.Range("A3").Value = "Average Match:"
    statsWs.Range("B3").Value = Format(avgMatch, "0.0%")
    statsWs.Range("A4").Value = "Highest Match:"
    statsWs.Range("B4").Value = Format(maxMatch, "0.0%")
    statsWs.Range("A5").Value = "Lowest Match:"
    statsWs.Range("B5").Value = Format(minMatch, "0.0%")
    
    MsgBox "Summary statistics created!"
End Sub

' ============================================
' MACRO 8: Conditional Formatting on Match %
' ============================================
Sub ApplyConditionalFormatting()
    Dim ws As Worksheet
    Dim dataRange As Range
    Dim lastRow As Long
    
    Set ws = ThisWorkbook.Sheets("Job Matches")
    lastRow = ws.Cells(ws.Rows.Count, "E").End(xlUp).Row
    Set dataRange = ws.Range("E2:E" & lastRow)
    
    ' Clear existing formatting
    dataRange.FormatConditions.Delete
    
    ' Add conditional formatting rules
    With dataRange.FormatConditions
        ' Green for >= 70%
        .Add Type:=xlCellValue, Operator:=xlGreaterEqual, Formula1:="70"
        .Item(1).Interior.Color = RGB(200, 230, 201)
        
        ' Yellow for 50-69%
        .Add Type:=xlCellValue, Operator:=xlBetween, Formula1:="50", Formula2:="69"
        .Item(2).Interior.Color = RGB(255, 249, 196)
        
        ' Orange for 30-49%
        .Add Type:=xlCellValue, Operator:=xlBetween, Formula1:="30", Formula2:="49"
        .Item(3).Interior.Color = RGB(255, 204, 188)
    End With
    
    MsgBox "Conditional formatting applied!"
End Sub

' ============================================
' MACRO 9: Quick Navigation Menu
' ============================================
Sub ShowNavigationMenu()
    Dim response As Integer
    
    response = MsgBox("Job Matcher Tools:" & vbCrLf & vbCrLf & _
        "1. Click OK to go to Dashboard" & vbCrLf & _
        "2. Click Cancel to go to Job Matches", vbOKCancel)
    
    If response = vbOK Then
        ThisWorkbook.Sheets("Dashboard").Activate
    Else
        ThisWorkbook.Sheets("Job Matches").Activate
    End If
End Sub

' ============================================
' MACRO 10: Export Top 10 to New Workbook
' ============================================
Sub ExportTop10()
    Dim ws As Worksheet
    Dim newWb As Workbook
    Dim newWs As Worksheet
    Dim topJobs As Range
    Dim i As Long
    
    Set ws = ThisWorkbook.Sheets("Top 10 Matches")
    Set newWb = Workbooks.Add
    Set newWs = newWb.Sheets(1)
    
    ' Copy header and top 10 data
    ws.Range("A1:E11").Copy
    newWs.Range("A1").PasteSpecial xlPasteAll
    
    ' Format new workbook
    With newWs.Rows(1)
        .Interior.Color = RGB(46, 125, 50)
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
    End With
    
    newWb.SaveAs ThisWorkbook.Path & "\Top_10_Jobs_" & Format(Now(), "yyyymmdd_hhmmss") & ".xlsx"
    MsgBox "Top 10 exported to new workbook!"
End Sub
