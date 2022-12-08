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

        // document.getElementById('mainDiv').appendChild(divElem);

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
    
}

function deploy(event){
    console.log('Deploy');
    console.log(event.currentTarget.parentNode);
}

function getUsers(event){
    console.log('GetUsers');
    console.log(event.currentTarget.parentNode);
}

function kickUsers(event){
    console.log('KickUsers');
    console.log(event.currentTarget.parentNode);
}

// event.currentTarget.parentNode.parentNode.remove();
// event.currentTarget.closest('div').remove();
// $.ajax({
//     url: "http://localhost:5000/servers",
//     success: function(response){
//         console.log(event.currentTarget);
//     }
// });

// 1) Update Build Info with refresh
//      a. Test ajax function to API /refresh
//      b. update table without refresh ez.
// 2) Test functionality of changing table (including creating or removing table) upon deployment and change of version
// 3) Popup windows for deploy, get logged in users, kick users,