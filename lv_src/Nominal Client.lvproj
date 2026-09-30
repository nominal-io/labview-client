<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="20008000">
	<Property Name="CCSymbols" Type="Str">Nominal_Debug_File,TRUE;Nominal_Debug_Trace,FALSE;Nominal_Disable_Comms,FALSE;</Property>
	<Property Name="NI.LV.All.SaveVersion" Type="Str">20.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Examples" Type="Folder">
			<Item Name="support" Type="Folder">
				<Item Name="PID Control.vi" Type="VI" URL="../Examples/PID Control.vi"/>
				<Item Name="Nominal Deadband Simulator.vi" Type="VI" URL="../Examples/Nominal Deadband Simulator.vi"/>
				<Item Name="Nominal Plant System.vi" Type="VI" URL="../Examples/Nominal Plant System.vi"/>
				<Item Name="periodic_trigger.vi" Type="VI" URL="../support/periodic_trigger.vi"/>
				<Item Name="PID Controller.vi" Type="VI" URL="../support/PID Controller.vi"/>
			</Item>
			<Item Name="Connect and Disconnect.vi" Type="VI" URL="../Examples/Connect and Disconnect.vi"/>
			<Item Name="Multipart Upload.vi" Type="VI" URL="../Nominal Client/Multipart Upload.vi"/>
			<Item Name="Simple - Create Data Source.vi" Type="VI" URL="../Examples/Simple - Create Data Source.vi"/>
			<Item Name="Simple - Get All Units.vi" Type="VI" URL="../Examples/Simple - Get All Units.vi"/>
			<Item Name="Simple - Runs.vi" Type="VI" URL="../Examples/Simple - Runs.vi"/>
			<Item Name="Simple - Upload File.vi" Type="VI" URL="../Examples/Simple - Upload File.vi"/>
			<Item Name="Simple - Write Data.vi" Type="VI" URL="../Examples/Simple - Write Data.vi"/>
			<Item Name="Streaming - Write.vi" Type="VI" URL="../Examples/Streaming - Write.vi"/>
			<Item Name="Streaming - Write Custom Cluster.vi" Type="VI" URL="../Examples/Streaming - Write Custom Cluster.vi"/>
			<Item Name="Workspaces.vi" Type="VI" URL="../Examples/Workspaces.vi"/>
			<Item Name="Test Centric Run Workflow.vi" Type="VI" URL="../Examples/Test Centric Run Workflow.vi"/>
		</Item>
		<Item Name="Quick Start" Type="Folder">
			<Property Name="NI.SortType" Type="Int">3</Property>
			<Item Name="Quick Start - Workspaces.vi" Type="VI" URL="../Quick Start/Quick Start - Workspaces.vi"/>
			<Item Name="Quick Start - Connect and Disconnect.vi" Type="VI" URL="../Quick Start/Quick Start - Connect and Disconnect.vi"/>
			<Item Name="Quick Start - Deadband Simulator.vi" Type="VI" URL="../Quick Start/Quick Start - Deadband Simulator.vi"/>
			<Item Name="Quick Start - Nominal Plant System.vi" Type="VI" URL="../Quick Start/Quick Start - Nominal Plant System.vi"/>
			<Item Name="Quick Start - PID Control.vi" Type="VI" URL="../Quick Start/Quick Start - PID Control.vi"/>
			<Item Name="Quick Start - Simple - Create Data Source.vi" Type="VI" URL="../Quick Start/Quick Start - Simple - Create Data Source.vi"/>
			<Item Name="Quick Start - Simple - Get All Units.vi" Type="VI" URL="../Quick Start/Quick Start - Simple - Get All Units.vi"/>
			<Item Name="Quick Start - Simple - Upload File.vi" Type="VI" URL="../Quick Start/Quick Start - Simple - Upload File.vi"/>
			<Item Name="Quick Start - Simple - Upload Video.vi" Type="VI" URL="../Quick Start/Quick Start - Simple - Upload Video.vi"/>
			<Item Name="Quick Start - Run - Create.vi" Type="VI" URL="../Quick Start/Quick Start - Run - Create.vi"/>
			<Item Name="Quick Start - Runs - Get.vi" Type="VI" URL="../Quick Start/Quick Start - Runs - Get.vi"/>
			<Item Name="Quick Start - Runs - Add Data.vi" Type="VI" URL="../Quick Start/Quick Start - Runs - Add Data.vi"/>
			<Item Name="Quick Start - Complete Streaming with Datasource Creation.vi" Type="VI" URL="../Quick Start/Quick Start - Complete Streaming with Datasource Creation.vi"/>
			<Item Name="Quick Start - Write Custom Cluster.vi" Type="VI" URL="../Quick Start/Quick Start - Write Custom Cluster.vi"/>
			<Item Name="Tutorial - Tags and Properties.vi" Type="VI" URL="../Quick Start/Tutorial - Tags and Properties.vi"/>
			<Item Name="Quick Start - Update Channel Metadata.vi" Type="VI" URL="../Quick Start/Quick Start - Update Channel Metadata.vi"/>
		</Item>
		<Item Name="support" Type="Folder">
			<Item Name="create tdms file.vi" Type="VI" URL="../support/create tdms file.vi"/>
		</Item>
		<Item Name="timestampMetadata" Type="Folder">
			<Item Name="timestampMetadata.lvclass" Type="LVClass" URL="../timestampMetadata/timestampMetadata.lvclass"/>
			<Item Name="ts.relative.lvclass" Type="LVClass" URL="../ts.relative/ts.relative.lvclass"/>
			<Item Name="ts.absoloute.lvclass" Type="LVClass" URL="../ts.absoloute/ts.absoloute.lvclass"/>
			<Item Name="ts.epochOfTimeUnit.lvclass" Type="LVClass" URL="../ts.epochOfTimeUnit/ts.epochOfTimeUnit.lvclass"/>
			<Item Name="ts.iso8601.lvclass" Type="LVClass" URL="../ts.iso8601/ts.iso8601.lvclass"/>
			<Item Name="timestampType.lvclass" Type="LVClass" URL="../timestampType/timestampType.lvclass"/>
			<Item Name="ts.absoloute type.lvclass" Type="LVClass" URL="../ts.absoloute type/ts.absoloute type.lvclass"/>
			<Item Name="ts.logtime.lvclass" Type="LVClass" URL="../ts.logtime/ts.logtime.lvclass"/>
		</Item>
		<Item Name="Tests" Type="Folder">
			<Item Name="tdms file.vi" Type="VI" URL="../tests/tdms file.vi"/>
			<Item Name="test.workspace_create_datasource_and_connection_in_incorrect_workspace.vi" Type="VI" URL="../tests/test.workspace_create_datasource_and_connection_in_incorrect_workspace.vi"/>
			<Item Name="test.workspace_create_datasource_and_connection_in_expected_workspace.vi" Type="VI" URL="../tests/test.workspace_create_datasource_and_connection_in_expected_workspace.vi"/>
			<Item Name="test.workspace_create_datasource_and_connection_without_specifying_workspace.vi" Type="VI" URL="../tests/test.workspace_create_datasource_and_connection_without_specifying_workspace.vi"/>
			<Item Name="test.workspace_create_datasource_and_connection_specifying_default_workspace.vi" Type="VI" URL="../tests/test.workspace_create_datasource_and_connection_specifying_default_workspace.vi"/>
			<Item Name="test.workspace_create_datasource_without_workspace.vi" Type="VI" URL="../tests/test.workspace_create_datasource_without_workspace.vi"/>
			<Item Name="test.workspace_get.vi" Type="VI" URL="../tests/test.workspace_get.vi"/>
			<Item Name="test.timestamp_json.vi" Type="VI" URL="../tests/test.timestamp_json.vi"/>
			<Item Name="test.video injest payload.vi" Type="VI" URL="../tests/test.video injest payload.vi"/>
			<Item Name="test.ingest_dataflash.vi" Type="VI" URL="../tests/test.ingest_dataflash.vi"/>
			<Item Name="test.ingest_csv.vi" Type="VI" URL="../tests/test.ingest_csv.vi"/>
			<Item Name="test.ingest_journalJson.vi" Type="VI" URL="../tests/test.ingest_journalJson.vi"/>
			<Item Name="test.ingest_parquet.vi" Type="VI" URL="../tests/test.ingest_parquet.vi"/>
			<Item Name="test.ingest_video.vi" Type="VI" URL="../tests/test.ingest_video.vi"/>
			<Item Name="test.ingest_containerized.vi" Type="VI" URL="../tests/test.ingest_containerized.vi"/>
			<Item Name="test.ingest_mcapProtobufTimeseries.vi" Type="VI" URL="../tests/test.ingest_mcapProtobufTimeseries.vi"/>
			<Item Name="test.ingest_parquet 2.vi" Type="VI" URL="../tests/test.ingest_parquet 2.vi"/>
			<Item Name="test.ingest_csv 2.vi" Type="VI" URL="../tests/test.ingest_csv 2.vi"/>
			<Item Name="test.ingest_journalJSON v2.vi" Type="VI" URL="../tests/test.ingest_journalJSON v2.vi"/>
			<Item Name="asset create.vi" Type="VI" URL="../tests/asset create.vi"/>
			<Item Name="test type.vi" Type="VI" URL="../tests/test type.vi"/>
			<Item Name="test.event_create.vi" Type="VI" URL="../tests/test.event_create.vi"/>
			<Item Name="test.write_waveform.vi" Type="VI" URL="../tests/test.write_waveform.vi"/>
			<Item Name="test.assets_by_data_source.vi" Type="VI" URL="../tests/test.assets_by_data_source.vi"/>
			<Item Name="test.assets.vi" Type="VI" URL="../tests/test.assets.vi"/>
			<Item Name="test.write_log.vi" Type="VI" URL="../tests/test.write_log.vi"/>
		</Item>
		<Item Name="developer tools" Type="Folder">
			<Item Name="debugging project symbols.vi" Type="VI" URL="../developer tools/debugging project symbols.vi"/>
			<Item Name="open log file directory.vi" Type="VI" URL="../developer tools/open log file directory.vi"/>
			<Item Name="log file viewer.vi" Type="VI" URL="../developer tools/log file viewer.vi"/>
		</Item>
		<Item Name="non library methods" Type="Folder">
			<Item Name="type.property.set.vi" Type="VI" URL="../type/type.property.set.vi"/>
			<Item Name="assets.property.set.vi" Type="VI" URL="../asset/assets.property.set.vi"/>
		</Item>
		<Item Name="User Extensions" Type="Folder">
			<Item Name="GET Template.vi" Type="VI" URL="../Quick Start/Developer Extensions/GET Template.vi"/>
			<Item Name="POST Template.vi" Type="VI" URL="../Quick Start/Developer Extensions/POST Template.vi"/>
			<Item Name="PUT Template.vi" Type="VI" URL="../Quick Start/Developer Extensions/PUT Template.vi"/>
			<Item Name="DELETE Template.vi" Type="VI" URL="../Quick Start/Developer Extensions/DELETE Template.vi"/>
		</Item>
		<Item Name="User.lvclass" Type="LVClass" URL="../User/User.lvclass"/>
		<Item Name="asset.lvclass" Type="LVClass" URL="../asset/asset.lvclass"/>
		<Item Name="event.lvclass" Type="LVClass" URL="../event/event.lvclass"/>
		<Item Name="type.lvclass" Type="LVClass" URL="../type/type.lvclass"/>
		<Item Name="stream_custom_cluster.lvclass" Type="LVClass" URL="../stream_custom_cluster/stream_custom_cluster.lvclass"/>
		<Item Name="mcap.channel_locator.lvclass" Type="LVClass" URL="../mcap.channel_locator/mcap.channel_locator.lvclass"/>
		<Item Name="Multipart Upload.lvclass" Type="LVClass" URL="../Nominal Client MultiPart Upload/Multipart Upload.lvclass"/>
		<Item Name="Run.lvclass" Type="LVClass" URL="../Run/Run.lvclass"/>
		<Item Name="Nominal Client.lvclass" Type="LVClass" URL="../Nominal Client/Nominal Client.lvclass"/>
		<Item Name="datasources.lvlib" Type="Library" URL="../datasources/datasources.lvlib"/>
		<Item Name="nominal types.lvlib" Type="Library" URL="../nominal types/nominal types.lvlib"/>
		<Item Name="dataScopes.lvlib" Type="Library" URL="../nominal types/dataScope/dataScopes.lvlib"/>
		<Item Name="Nominal LabVIEW Client API Tree.vi" Type="VI" URL="../Nominal Client/Nominal LabVIEW Client API Tree.vi"/>
		<Item Name="Package Dependencies" Type="IIO Ladder Diagram">
			<Property Name="NI.SortType" Type="Int">0</Property>
			<Property Name="ShowPackages" Type="Bool">true</Property>
		</Item>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
