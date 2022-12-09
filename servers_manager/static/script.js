async function fetchServers () {
    return $.ajax({
        type: "GET",
        url: "http://localhost:5000/servers"
    });
}

async function loadTables() {
    const data = await fetchServers();
    for (const version of data){

        const divElem = document.createElement('div');

        divElem.setAttribute("id",version[0]['Version']);

        const versionElement = document.createElement('h1');

        versionElement.textContent = 'SPDRM ' + 'v' + version[0]['Version'];

        divElem.appendChild(versionElement);

        const tableElement = document.createElement('table');

        const theadElement = document.createElement('thead');

        const theadRowElement = document.createElement('tr');

        const h2Name = document.createElement('h2');
        const h2Interfaces = document.createElement('h2');
        const h2BuildInfo = document.createElement('h2');
        const h2Actions = document.createElement('h2');
        const h2Client = document.createElement('h2');

        h2Name.textContent = 'Name';
        h2Interfaces.textContent = 'Interfaces';
        h2BuildInfo.textContent = 'Build Info';
        h2Actions.textContent = 'Actions';
        h2Client.textContent = 'Client';

        const thName = document.createElement('th');
        const thInterfaces = document.createElement('th');
        const thBuildInfo = document.createElement('th');
        const thActions = document.createElement('th');
        const thClient = document.createElement('th');

        thName.appendChild(h2Name);
        thInterfaces.appendChild(h2Interfaces);
        thBuildInfo.appendChild(h2BuildInfo);
        thActions.appendChild(h2Actions);
        thClient.appendChild(h2Client);

        theadRowElement.appendChild(thName);
        theadRowElement.appendChild(thInterfaces);
        theadRowElement.appendChild(thBuildInfo);
        theadRowElement.appendChild(thActions);
        theadRowElement.appendChild(thClient);


        theadElement.appendChild(theadRowElement);
        tableElement.appendChild(theadElement);

        const tbodyElement = document.createElement('tbody');
        for (const server of version){
            const tbodyRowElement = document.createElement('tr');

            // Name
            const tdName = document.createElement('td');
            const h3Name = document.createElement('h3');
            h3Name.textContent = server['Name'];
            tdName.appendChild(h3Name);

            tbodyRowElement.appendChild(tdName);

            // Interfaces
            const tdInterface = document.createElement('td');

            const h3SPDRM = document.createElement('h3');
            const h3ADMIN = document.createElement('h3');
            const h3HOST = document.createElement('h3');

            h3SPDRM.textContent = 'SPDRM ' + server['Ws Port'];
            h3ADMIN.textContent = 'ADMIN ' + server['Admin Port'];
            h3HOST.textContent = 'HOST ' + server['Hostname'];

            const pSPDRM = document.createElement('p');
            const pADMIN = document.createElement('p');
            const pHOST = document.createElement('p');

            pSPDRM.appendChild(h3SPDRM);
            pADMIN.appendChild(h3ADMIN);
            pHOST.appendChild(h3HOST);
            
            const aSPDRM = document.createElement('a');
            const aADMIN = document.createElement('a');

            aSPDRM.appendChild(pSPDRM);
            aSPDRM.href = "http://" + server['Hostname'] + ":" + server['Ws Port'] + "/spdrm/";
            aSPDRM.target = '_blank';

            aADMIN.appendChild(pADMIN);
            aADMIN.href = "http://" + server['Hostname'] + ":" +server['Admin Port'];
            aADMIN.target = '_blank';

            tdInterface.appendChild(aSPDRM);
            tdInterface.appendChild(aADMIN);
            tdInterface.appendChild(pHOST);

            tbodyRowElement.appendChild(tdInterface);

            // Build Info
            const tdBuildInfo = document.createElement('td');
            
            const h3Version = document.createElement('h3');
            const h3BuildDate = document.createElement('h3'); 
            const h3PE = document.createElement('h3');
            const h3DM = document.createElement('h3');
            const h3KB = document.createElement('h3');

            
            h3Version.textContent = 'Version ' + server['Version'];
            h3BuildDate.textContent = 'Build Date ' + server['built_date'];
            h3PE.textContent = 'Process Enabled ' + server['process_enabled'];
            h3DM.textContent = 'DM Enabled ' + server['dm_enabled'];
            h3KB.textContent = 'KB Enabled ' + server['kb_enabled'];

            const pVersion = document.createElement('p');
            const pBuildDate = document.createElement('p');
            const pPE = document.createElement('p');
            const pDM = document.createElement('p');
            const pKB = document.createElement('p');

            pVersion.appendChild(h3Version);
            pBuildDate.appendChild(h3BuildDate);
            pPE.appendChild(h3PE);
            pDM.appendChild(h3DM);
            pKB.appendChild(h3KB);

            tdBuildInfo.appendChild(pVersion);
            tdBuildInfo.appendChild(pBuildDate);
            tdBuildInfo.appendChild(pPE);
            tdBuildInfo.appendChild(pDM);
            tdBuildInfo.appendChild(pKB);

            tbodyRowElement.appendChild(tdBuildInfo);

            // Actions
            const tdActions = document.createElement('td');
            
            const h3Refresh = document.createElement('h3');
            const h3Deploy =document.createElement('h3');
            const h3GetUsers = document.createElement('h3');
            const h3KickUsers = document.createElement('h3');
            

            h3Refresh.textContent = 'Refresh';
            h3Deploy.textContent = 'Deploy';
            h3GetUsers.textContent = 'Get Logged In Users';
            h3KickUsers.textContent = 'Kick Users';

            const pRefresh = document.createElement('p');
            const pDeploy = document.createElement('p');
            const pGetUsers = document.createElement('p');
            const pKickUsers = document.createElement('p');

            pRefresh.appendChild(h3Refresh);
            pDeploy.appendChild(h3Deploy);
            pGetUsers.appendChild(h3GetUsers);
            pKickUsers.appendChild(h3KickUsers);
            
            const aRefresh = document.createElement('a');
            aRefresh.addEventListener("click", refresh, false);

            const aDeploy = document.createElement('a');
            aDeploy.addEventListener("click", deploy, false);

            const aGetUsers = document.createElement('a');
            aGetUsers.addEventListener("click", getUsers, false);

            const aKickUsers = document.createElement('a');
            aKickUsers.addEventListener("click", kickUsers, false);

            aRefresh.appendChild(pRefresh);
            aDeploy.appendChild(pDeploy);
            aGetUsers.appendChild(pGetUsers);
            aKickUsers.appendChild(pKickUsers);

            tdActions.appendChild(aRefresh);
            tdActions.appendChild(aDeploy);
            tdActions.appendChild(aGetUsers);
            tdActions.appendChild(aKickUsers);

            tbodyRowElement.appendChild(tdActions);

            // Client
            const tdClient = document.createElement('td');
            const h3Client = document.createElement('h3');
            h3Client.textContent = server['Client Path'];
            tdClient.appendChild(h3Client);
            tbodyRowElement.appendChild(tdClient);
 
            // Attach Row to Body to Document
            tbodyElement.appendChild(tbodyRowElement);
            tableElement.appendChild(tbodyElement);
            divElem.appendChild(tableElement)
            document.getElementById('mainDiv').appendChild(divElem);
        }
    }
}


function refresh(event){
    console.log('Refresh');
    var ws_port = event.currentTarget.parentNode.parentNode.cells[1].childNodes[0].firstChild.firstChild.textContent.split(" ")[1];
    var host = event.currentTarget.parentNode.parentNode.cells[1].childNodes[2].firstChild.textContent.split(" ")[1];
    let data = {
        "port": ws_port,
        "host": host
    };

    var row = event.currentTarget.parentNode.parentNode;

    $.ajax({
        url: "http://localhost:5000/refresh",
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (response){
            changeRow(response, row);
        }
    });
}

function changeRow(response, row){
    const currentVersion = row.cells[2].childNodes[0].firstChild.firstChild.textContent.split(" ")[1];
    
    if(response['version'] != currentVersion){
         // Remove div current version has only one row
         const currentDiv = document.getElementById(currentVersion);
         if (currentDiv.childNodes[1].childNodes[1].childNodes.length == 1){
            currentDiv.remove();
         }

         const newDiv = document.getElementById(response['version']);

         row.cells[2].childNodes[0].firstChild.firstChild.textContent = 'Version ' + response['version'];
         row.cells[2].childNodes[1].firstChild.firstChild.textContent = 'Build Date ' + response['built_date'];
         row.cells[2].childNodes[2].firstChild.firstChild.textContent = 'Process Enabled ' + response['process_enabled'];
         row.cells[2].childNodes[3].firstChild.firstChild.textContent = 'DM Enabled ' + response['dm_enabled'];
         row.cells[2].childNodes[4].firstChild.firstChild.textContent = 'KB Enabled ' + response['kb_enabled'];


         // If does not exist create new div, table
         if (newDiv == null){
            currentDiv.setAttribute("id", response['version']);
            currentDiv.childNodes[0].firstChild.textContent = 'SPDRM ' + 'v' + response['version'];
            currentDiv.childNodes[1].childNodes[1].childNodes[0] = row;


            for(let i = 0 ; i < document.getElementById('mainDiv').children.length ; i++){
                
                if(document.getElementById('mainDiv').children[i].getAttribute("id").localeCompare(response['version']) == -1){
                    document.getElementById('mainDiv').children[i].before(currentDiv);
                    break;
                }
                
                if(i == document.getElementById('mainDiv').children.length - 1){
                    document.getElementById('mainDiv').children[i].after(currentDiv);
                    break;
                }
            }


         } else {
            // Update table of new version with the current server
            newDiv.childNodes[1].childNodes[1].appendChild(row);
         }

         
    } else {
        // Update just the row in current version table.
        row.cells[2].childNodes[1].firstChild.firstChild.textContent = 'Build Date ' + response['built_date'];
        row.cells[2].childNodes[2].firstChild.firstChild.textContent = 'Process Enabled ' + response['process_enabled'];
        row.cells[2].childNodes[3].firstChild.firstChild.textContent = 'DM Enabled ' + response['dm_enabled'];
        row.cells[2].childNodes[4].firstChild.firstChild.textContent = 'KB Enabled ' + response['kb_enabled'];
    }
}


function deploy(event){
    console.log('Deploy');
    console.log(event.currentTarget.parentNode);
    // var response = 
}

function getUsers(event){
    console.log('GetUsers');
    console.log(event.currentTarget.parentNode);
}

function kickUsers(event){
    console.log('KickUsers');
    console.log(event.currentTarget.parentNode);
}


// 4) Popup windows for deploy, get logged in users, kick users,
// 5) From 'version' to 'Version' and vice versa.