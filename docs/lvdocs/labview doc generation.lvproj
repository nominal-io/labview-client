<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="20008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">20.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="misc" Type="Folder">
			<Item Name="convert palette names into relative paths.vi" Type="VI" URL="../convert palette names into relative paths.vi"/>
			<Item Name="dump data from VIs.vi" Type="VI" URL="../dump data from VIs.vi"/>
			<Item Name="get ID from vi.vi" Type="VI" URL="../get ID from vi.vi"/>
			<Item Name="get palette sections with items.vi" Type="VI" URL="../get palette sections with items.vi"/>
			<Item Name="get palettes.vi" Type="VI" URL="../get palettes.vi"/>
			<Item Name="simple element vs typedef.vi" Type="VI" URL="../simple element vs typedef.vi"/>
		</Item>
		<Item Name="types" Type="Folder">
			<Item Name="sphinx item data.ctl" Type="VI" URL="../sphinx item data.ctl"/>
			<Item Name="sphinx terminal data.ctl" Type="VI" URL="../sphinx terminal data.ctl"/>
			<Item Name="sphinx terminal direction.ctl" Type="VI" URL="../sphinx terminal direction.ctl"/>
			<Item Name="sphinx terminal requiredness.ctl" Type="VI" URL="../sphinx terminal requiredness.ctl"/>
		</Item>
		<Item Name="export example information.vi" Type="VI" URL="../export example information.vi"/>
		<Item Name="export labview dosctrings.vi" Type="VI" URL="../export labview dosctrings.vi"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
