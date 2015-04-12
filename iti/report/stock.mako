<html>
<head>
     <style type="text/css">${css}</style>
</head>
<body>
    <h2>Stock Report</h2>
    <table border="2">
        <tr>
            <th>
                Suppliers
            </th>
            <th>
                Product
            </th>
            <th>
                deficit
            </th>
            <th>
                surplus
            </th>
        </tr>
         % for session in objects :
            <tr>
                <td> ${ session.suppliers_ids } </td>
                <td>${ session.name }</td>
                % if session.qty_available  >  session.max_qty:

                    <td>nothing</td>
                    <td>${ session.qty_available } - ${ session.max_qty }</td>

                % elif session.qty_available < session.min_qty:

                    <td>${ session.qty_available } - ${ session.min_qty }</td>
                    <td>nothing</td>

                % else:

                    <td>nothing</td>
                    <td>nothing</td>
                % endif

            </tr>
        % endfor
    </table>
</body>
</html>
